import pickle
import importlib
import os
import threading
import sys
import time

import bottle

from objects import User
import modules
import config
from modules import iplib, logging, extract_traceback
import dbutils
import models.notifications
import models
import models.seo_info


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


class PageBuilder:
    def __init__(self, template_name:str, **kwargs):
        self._template_name = template_name
        self._kwargs = kwargs
        auth.set_user(self)
        seo_info = models.seo_info.get(template_name)
        if seo_info:
            self.add_param('seo_info', seo_info)
        self.add_param('serverinfo', {'ip': config.server.ip, 'port': config.server.port})
        self.add_param('tplname', template_name)

    def add_param(self, name:str, value):
        self._kwargs[name] = value

    def template(self):
        if os.path.exists(os.path.join(config.server_root, 'views', self._template_name + '_head.tpl')):
            return bottle.template(self._template_name, header_name=self._template_name + '_head.tpl', **self._kwargs)
        return bottle.template(self._template_name, **self._kwargs)


class templates:
    @staticmethod
    def permission_denied(text:str='Доступ ограничен',
                          description:str='Вы не можете просматривать эту страницу') -> PageBuilder:
        return templates.message(text, description)

    @staticmethod
    def message(text:str, description:str) -> PageBuilder:
        return PageBuilder("text", message=text, description=description)


def denypost(func):
    def wrapper(*args, **kwargs):
        serveraddr = 'http://{}'.format(config.server.ip)
        if bottle.request.method.lower() == 'post' and not bottle.request.get_header('Referer',
                                                                                     serveraddr).startswith(
                serveraddr):
            try:
                raise ValueError('POST request from other domain')
            except Exception as e:
                logging.error(e)
            raise bottle.HTTPError(404)  # TODO: refactor
        return func(*args, **kwargs)

    return wrapper


def access_and_error_log(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        try:
            response = func(*args, **kwargs)
            logging.access(time.time() - t)
            return response
        except (bottle.HTTPError, bottle.HTTPResponse) as e:
            logging.access(time.time() - t)
            raise e
        except Exception as e:
            logging.error(e, time.time() - t)
            if config.debug:
                return templates.message(e.__class__.__name__,
                                         extract_traceback(e, '<br>').replace('\n', '<br>')).template()
            return templates.message("Возникла непредвиденная ошибка", "Сообщите нам об этом, пожалуйста.").template()

    return wrapper


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
    @access_and_error_log
    @iplib.ipfilter
    @denypost
    def execute(self, **kwargs):
        with self._lock:
            return self._page.execute(bottle.request.method, **kwargs)


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
                modules.logging.error(e)


def set_cookie(name:str, value):
    return bottle.response.set_cookie(name, value, config.secret)


def get_cookie(name:str, default=None):
    return bottle.request.get_cookie(name, default, config.secret)


class _MockUserLevel(set):
    @staticmethod
    def admin() -> bool:
        return False

    @staticmethod
    def organizer() -> bool:
        return False

    @staticmethod
    def responsible() -> bool:
        return False

    @staticmethod
    def common() -> bool:
        return False

    @staticmethod
    def judge() -> bool:
        return False

    @staticmethod
    def resporgadmin() -> bool:
        return False

    def __contains__(self, item):
        return False


class _MockUser:
    def user_id(self) -> int:
        return 0

    @property
    def userlevel(self) -> _MockUserLevel:
        return _MockUserLevel


class _AuthDispatcher:
    def set_user(self, page_builder:PageBuilder):
        page_builder.add_param('current_user', self.current())
        page_builder.add_param('loggedin', self.loggedin())
        if self.loggedin():
            page_builder.add_param('notifycount', models.notifications.get_count(self.current().user_id()))


    def login(self, email:str, password:str):
        if self.loggedin(): return
        with dbutils.dbopen() as db:
            user = db.execute(
                "SELECT * FROM users WHERE email='{}' AND passwd='{}'".format(
                    email, password), dbutils.dbfields['users'])
            if len(user) == 0:
                raise ValueError("Invalid email or password")
            db.execute("UPDATE users SET lasttime=NOW() WHERE user_id={}".format(user[0]['user_id']))
            set_cookie('user', pickle.dumps(user[0]))

    def logout(self):
        bottle.response.delete_cookie('user')

    def loggedin(self) -> bool:
        user = get_cookie('user')
        return not (user is None)

    def current(self) -> User:
        if not self.loggedin(): return _MockUser()
        return User(pickle.loads(get_cookie('user')))

    def reloaduser(self, user:dict):
        # bottle.response.delete_cookie('user')
        set_cookie('user', pickle.dumps(user))

    def __bool__(self):
        return self.loggedin()


controller = _PageController()
auth = _AuthDispatcher()