import importlib
import os
import threading
import sys

import bottle

import modules
import modules.dbutils
import modules.logging
from modules.utils import get_notifycount



# +-> _Executor.execute -> page.execute
# bottle routing -|
# +-> _Executor.execute -> page.execute
# ....


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
                return self._page.execute(bottle.request.method, **kwargs)
            except (bottle.HTTPError, bottle.HTTPResponse) as e:
                raise e
            except Exception as e:
                try:
                    modules.logging.error(self.name + ' - ' + e.__class__.__name__ + ': {}',
                                          e.args[0] if len(e.args) > 0 else '')
                    modules.logging.info(modules.extract_traceback(e))
                except Exception as er:
                    modules.logging.error(
                        'Error while handling <{}> error: {}'.format(e.__class__.__name__, er.__class__.__name__))
                raise bottle.HTTPError(404)


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
        if not page_class:
            modules.logging.warn('Subclass of Page is not found in {}', module)
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
            except ImportError as e:
                modules.logging.error('Import error of <{}>: {}', module_name, e.args[0])


class _AuthDispatcher:
    def set_user(self, page_builder):
        userinfo = dict()
        userinfo['user_id'] = self.getuserid()
        userinfo['adminlevel'] = self.getadminlevel()
        userinfo['notifycount'] = get_notifycount(self.getuserid())
        userinfo['organizer'] = self.organizer()
        userinfo['responsible'] = self.responsible()
        userinfo['common'] = self.common()
        page_builder.add_param('userinfo', userinfo)
        page_builder.add_param('loggedin', self.loggedin())

    def login(self, email:str, password:str):
        if self.loggedin(): return
        with modules.dbutils.dbopen() as db:
            user = db.execute(
                "SELECT user_id, admin FROM users WHERE email='{}' AND passwd='{}'".format(email, password),
                ['user_id', 'adminlevel'])
            if len(user) == 0:
                raise ValueError("Invalid email or password")
            user = user[0]
            db.execute("UPDATE users SET lasttime=NOW() WHERE user_id={}".format(user['user_id']))
            bottle.response.set_cookie('user_id', user['user_id'], modules.config['secret'])
            bottle.response.set_cookie('adminlevel', user['adminlevel'], modules.config['secret'])

    def logout(self):
        bottle.response.delete_cookie('user_id')
        bottle.response.delete_cookie('adminlevel')

    def getuserid(self) -> int:
        return int(bottle.request.get_cookie('user_id', 0, modules.config['secret']))

    def getadminlevel(self) -> int:
        return int(bottle.request.get_cookie('adminlevel', 0, modules.config['secret']))

    def loggedin(self) -> bool:
        return bool(self.getuserid())

    def organizer(self) -> bool:
        return self.loggedin() and self.getadminlevel() == 1

    def responsible(self) -> bool:
        return self.loggedin() and (self.getadminlevel() == 2 or self.organizer())

    def common(self) -> bool:
        return self.loggedin() and (self.getadminlevel() == 3 or self.responsible() or self.organizer())


class PageBuilder:
    def __init__(self, template_name:str, header_name:str='_basichead', **kwargs):
        self._template_name = template_name
        self._header_name = header_name
        self._kwargs = kwargs
        auth_dispatcher.set_user(self)

    def add_param(self, name:str, value):
        self._kwargs[name] = value

    def template(self):
        return bottle.template(self._template_name, header_name=self._header_name, **self._kwargs)


controller = _PageController()
auth_dispatcher = _AuthDispatcher()