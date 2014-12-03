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


def log(func):
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


def deny_post(func):
    def wrapper(*args, **kwargs):
        raise NotImplementedError # TODO
    return wrapper


@iplib.ipfilter
@log
def execute(func, *args, **kwargs):
    data = func(*args, **kwargs)
    if isinstance(data, PageBuilder):
        return data.template()
    return data


@property
def referer():
    return bottle.request.get_header('Referer', '/')


def route(path=None, method='GET', name=None, apply=None, skip=None, **kwconfig):
    def decorator(func):
        def wrapper(*args, **kwargs):
            return execute(func, *args, **kwargs)
        if isinstance(path, str):
            bottle.route(path=path, method=method, callback=wrapper, name=name, apply=apply, skip=skip, **kwconfig)
        else:
            for p in path:
                bottle.route(path=p, method=method, callback=wrapper, name=name, apply=apply, skip=skip, **kwconfig)
        return wrapper
    return decorator


def get(path=None, name=None, apply=None, skip=None, **kwconfig):
    return route(path=path, name=name, apply=apply, skip=skip, **kwconfig)


def post(path=None, name=None, apply=None, skip=None, **kwconfig):
    return route(path=path, method='POST', name=name, apply=apply, skip=skip, **kwconfig)


def only_admins(func):
    def wrapper(*args, **kwargs):
        if not auth.current().userlevel.admin():
            return templates.permission_denied()
        return func(*args, **kwargs)
    return wrapper


def only_organizers(func):
    def wrapper(*args, **kwargs):
        if not auth.current().userlevel.admin() and not auth.current().userlevel.organizer():
            return templates.permission_denied()
        return func(*args, **kwargs)
    return wrapper


def only_loggedin(func):
    def wrapper(*args, **kwargs):
        if not auth.loggedin():
            return templates.not_loggedin()
        return func(*args, **kwargs)
    return wrapper


def only_ajax(func):
    def wrapper(*args, **kwargs):
        if not bottle.request.is_ajax:
            raise bottle.HTTPError(404)
        return func(*args, **kwargs)
    return wrapper


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

    def param(self, name:str):
        return self._kwargs[name]

    def __contains__(self, item):
        return item in self._kwargs

    def template(self):
        if self._search_head(self._template_name + '_head.tpl'):
            return bottle.template(self._template_name, header_name=self._template_name + '_head.tpl', **self._kwargs)
        return bottle.template(self._template_name, **self._kwargs)

    def _search_head(self, tplname:str):
        return any(map(lambda x: os.path.exists(os.path.join(x, tplname)), config.paths.server.views))


class templates:
    @staticmethod
    def permission_denied(text:str='Доступ ограничен',
                          description:str='Вы не можете просматривать эту страницу') -> PageBuilder:
        return templates.message(text, description)

    @staticmethod
    def not_loggedin():
        return templates.permission_denied(description='Доступно только зарегестрированным пользователям')

    @staticmethod
    def message(text:str, description:str) -> PageBuilder:
        return PageBuilder("text", message=text, description=description)


def set_cookie(name:str, value):
    return bottle.response.set_cookie(name, value, config.secret, max_age=604800, path='/')


def get_cookie(name:str, default=None):
    return bottle.request.get_cookie(name, default, config.secret)


def delete_cookie(name:str):
    return bottle.response.delete_cookie(name)


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
            page_builder.add_param('notifycount', models.notifications.get_count(self.current().user_id())) # TODO: CACHE!


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
        return bool(get_cookie('user'))

    def current(self) -> User:
        if not self.loggedin(): return _MockUser()
        return User(pickle.loads(get_cookie('user')))

    def reloaduser(self, user:dict):
        # bottle.response.delete_cookie('user')
        set_cookie('user', pickle.dumps(user))

    def __bool__(self):
        return self.loggedin()


for module_name in os.listdir(os.path.join(config.paths.server.root, 'pages')):
    if module_name.startswith('_'):
        continue
    try:
        module_name = os.path.splitext(module_name)[0]
        importlib.import_module('pages.{}'.format(module_name))
    except Exception as e:
        modules.logging.error(e)

auth = _AuthDispatcher()

