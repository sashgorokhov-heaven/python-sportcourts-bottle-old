import bottle

import importlib
import os
import threading
import sys
import modules
import modules.logging
import modules.dbutils
import models.notifications
import models.settings
from models import mailing

class Page:  # this name will be reloaded by PageController.reload(name='Page')
    def execute(self, method:str, **kwargs):
        if method == 'POST':
            data = self.post(**kwargs)
            if isinstance(data, PageBuilder):
                return data.template()
            return data
        if method == 'GET':
            data = self.get(**kwargs)
            if isinstance(data, PageBuilder):
                return data.template()
            return data
        raise bottle.HTTPError(404)

    def get(self, **kwargs):  # name='alex'
        raise bottle.HTTPError(404)

    def post(self, **kwargs):
        raise bottle.HTTPError(404)

    get.route = ''  # /hello/<name> - /hello/alex
    post.route = ''


class _Executor:
    def __init__(self, page:Page):
        self._lock = threading.Lock()
        self._page = None
        self.set_page(page)

    def page(self):
        with self._lock:
            return self._page

    def set_page(self, page:Page):
        with self._lock:
            if self._page:
                del self._page
            self._page = page
            self.name = self._page.__class__.__name__


    # @route(self._page.get.route)
    # @route(self._page.post.route)
    def execute(self, **kwargs):
        with self._lock:
            try:
                modules.logging.access_log()
                return self._page.execute(bottle.request.method, **kwargs)
            except (bottle.HTTPError, bottle.HTTPResponse) as e:
                raise e
            except Exception as e:
                modules.logging.error_log(e)
                mailing.send_report(e)
                if modules.config['debug']:
                    return templates.message(e.__class__.__name__,
                                             modules.extract_traceback(e, '<br>').replace('\n', '<br>')).template()
                return templates.message("Возникла непредвиденная ошибка", "Сообщите нам о ней, пожалуйста.").template()


class _PageController:
    def __init__(self):
        self._executors = dict()
        self.loadpages()

    def add_page(self, page_class:type):
        instance = page_class()
        executor = _Executor(instance)
        self._executors[executor.name] = executor
        if instance.get.route:
            bottle.get(instance.get.route, callback=executor.execute)  # <------ Route mount point
        if instance.post.route:
            bottle.post(instance.post.route, callback=executor.execute)  # <------ Route mount point

    def reload(self, name:str) -> type:
        if name not in self._executors:
            raise ValueError('Executor on <{}> not registered'.format(name))
        executor = self._executors[name]
        module_name = executor.page().__class__.__module__
        module = sys.modules[module_name]
        reloaded = importlib.reload(module)
        page_class = self._search_module(reloaded)
        if page_class:
            executor.set_page(page_class())

    def _search_module(self, module) -> type:
        page_class = None
        for smthing in dir(module):
            if not smthing.startswith('_') \
                    and type(getattr(module, smthing)) == type(Page) \
                    and issubclass(getattr(module, smthing), Page) \
                    and getattr(module, smthing).__module__.startswith('pages.'):
                page_class = getattr(module, smthing)
                break
        return page_class

    def loadpages(self):
        for module_name in os.listdir('pages'):
            if module_name.startswith('_'):
                continue
            try:
                module_name = os.path.splitext(module_name)[0]
                module = importlib.import_module('pages.{}'.format(module_name))
                page_class = self._search_module(module)
                if page_class and page_class.__name__ not in self._executors:
                    self.add_page(page_class)
            except Exception as e:
                modules.logging.error_log(e, 'Import error of <{}>'.format(module_name))


class _AuthDispatcher:
    def set_user(self, page_builder):
        userinfo = dict()
        userinfo['user_id'] = self.getuserid()
        userinfo['userlevel'] = self.getuserlevel()
        userinfo['username'] = self.getusername()
        userinfo['usersex'] = self.getusersex()
        userinfo['notifycount'] = models.notifications.get_count(self.getuserid())
        userinfo['admin'] = self.admin()
        userinfo['usersettings'] = self.getusersettings()
        userinfo['organizer'] = self.organizer()
        userinfo['responsible'] = self.responsible()
        userinfo['common'] = self.common()
        page_builder.add_param('userinfo', userinfo)
        page_builder.add_param('loggedin', self.loggedin())

    def login(self, email:str, password:str):
        if self.loggedin(): return
        with modules.dbutils.dbopen() as db:
            user = db.execute(
                "SELECT * FROM users WHERE email='{}' AND passwd='{}'".format(
                    email, password), modules.dbutils.dbfields['users'])
            if len(user) == 0:
                raise ValueError("Invalid email or password")
            user = user[0]
            db.execute("UPDATE users SET lasttime=NOW() WHERE user_id={}".format(user['user_id']))
            # secretkey = base64.b16encode(bottle.request.remote_addr).decode()+modules.config['secret']
            bottle.response.set_cookie('user_id', user['user_id'], modules.config['secret'])
            bottle.response.set_cookie('userlevel', user['userlevel'], modules.config['secret'])
            bottle.response.set_cookie('usersex', user['sex'], modules.config['secret'])
            bottle.response.set_cookie('usersettings', user['settings'], modules.config['secret'])
            bottle.response.set_cookie('username', user['first_name'] + ' ' + user['last_name'],
                                       modules.config['secret'])

    def logout(self):
        bottle.response.delete_cookie('user_id')
        bottle.response.delete_cookie('userlevel')
        bottle.response.delete_cookie('username')
        bottle.response.delete_cookie('usersettings')
        bottle.response.delete_cookie('usersex')

    def getuserid(self) -> int:
        return int(bottle.request.get_cookie('user_id', 0, modules.config['secret']))

    def getusername(self) -> str:
        return bottle.request.get_cookie('username', 'Unknown Username', modules.config['secret'])

    def getusersex(self) -> str:
        return bottle.request.get_cookie('usersex', 'male', modules.config['secret'])

    def getuserlevel(self) -> int:
        return int(bottle.request.get_cookie('userlevel', 0, modules.config['secret']))

    def updatesettings(self, sett:models.settings.SettingsClass=None, dbconnection:modules.dbutils.DBConnection=None):
        if not sett:
            bottle.response.set_cookie('usersettings',
                                       models.settings.get(self.getuserid(), dbconnection=dbconnection).format(),
                                       modules.config['secret'])
        else:
            bottle.response.set_cookie('usersettings', sett.format(), modules.config['secret'])

    def getusersettings(self) -> models.settings.SettingsClass:
        return models.settings.SettingsClass(
            bottle.request.get_cookie('usersettings', models.settings.default().format(), modules.config['secret']))

    def loggedin(self) -> bool:
        return bool(self.getuserid())

    def admin(self) -> bool:
        return self.loggedin() and self.getuserlevel() == 0

    def organizer(self) -> bool:
        return self.loggedin() and (self.getuserlevel() == 1 or self.admin())

    def responsible(self) -> bool:
        return self.loggedin() and (self.getuserlevel() == 2 or self.organizer() or self.admin())

    def common(self) -> bool:
        return self.loggedin() and (self.getuserlevel() == 3 or self.responsible() or self.organizer() or self.admin())


class PageBuilder:
    def __init__(self, template_name:str, **kwargs):
        self._template_name = template_name
        self._kwargs = kwargs
        auth_dispatcher.set_user(self)
        self.add_param('serverinfo', modules.config['server'])

    def add_param(self, name:str, value):
        self._kwargs[name] = value

    def template(self):
        if os.path.exists(os.path.join(modules.config['server_root'], 'views', self._template_name + '_head.tpl')):
            return bottle.template(self._template_name, header_name=self._template_name + '_head.tpl', **self._kwargs)
        return bottle.template(self._template_name, **self._kwargs)


class _CompleteTemplates:
    def permission_denied(self, text:str='Доступ ограничен',
                          description:str='Вы не можете просматривать эту страницу') -> PageBuilder:
        return self.message(text, description)

    def message(self, text:str, description:str) -> PageBuilder:
        return PageBuilder("text", message=text, description=description)


controller = _PageController()
auth_dispatcher = _AuthDispatcher()
templates = _CompleteTemplates()