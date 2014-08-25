import importlib
import os
import threading
import sys

import bottle

import modules
import modules.dbutils
import modules.logging
from modules.utils import get_notifycount


def getuserid() -> int:
    return int(bottle.request.get_cookie('user_id', 0, modules.config['secret']))


def getadminlevel() -> int:
    return int(bottle.request.get_cookie('adminlevel', 0, modules.config['secret']))


def loggedin() -> bool:
    return bool(getuserid())


def activated() -> bool:
    return bool(int(bottle.request.get_cookie('activated', 0, modules.config['secret'])))


def user_type() -> str:
    return str(bottle.request.get_cookie('user_type', 'common', modules.config['secret']))


def setlogin(func):
    def wrapper(*args, **kwargs):
        template = func(*args, **kwargs)
        if not isinstance(template, Template):
            return template
        user_id = getuserid()
        template.add_parameter('user_id', user_id)
        template.add_parameter('loggedin', bool(user_id))
        template.add_parameter('adminlevel', getadminlevel())
        template.add_parameter('activated', activated())
        template.add_parameter('notifycount', get_notifycount(user_id))
        return template
    return wrapper


# +-> _Executor.execute -> page.execute
# bottle routing -|
#                 +-> _Executor.execute -> page.execute
#                ....


class Page: # this name will be reloaded by PageController.reload(name='Page')
    def execute(self, method:str, **kwargs):
        if method == 'POST':
            data = self.post(**kwargs)
            if isinstance(data, Template):
                return data.template()
            return data
        if method == 'GET':
            data = self.get(**kwargs)
            if isinstance(data, Template):
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
                    modules.logging.error(e.__class__.__name__ + ': {}', e.args[0] if len(e.args) > 0 else '')
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
        self._executors[page_class.__name__] = executor
        if instance.get.route:
            bottle.get(instance.get.route, callback=executor.execute)  # <------ Route mount point
        if instance.post.route:
            bottle.post(instance.post.route, callback=executor.execute)  # <------ Route mount point

    def reload(self, name:str):
        if name not in self._executors:
            raise ValueError('Executor on <{}> not registered'.format(name))
        module_name = self._executors[name].page().__class__.__module__
        module = sys.modules[module_name]
        reloaded = importlib.reload(module)
        sys.modules[module_name] = reloaded
        page_class = self._search_module(reloaded, module_name)
        if page_class:
            self._executors[page_class.__name__].set_page(page_class())

    def _search_module(self, module, module_name:str) -> type:
        page_class = None
        for smthing in dir(module):
            if not smthing.startswith('_') \
                    and type(getattr(module, smthing)) == type(Page) \
                    and issubclass(getattr(module, smthing), Page) \
                    and getattr(module, smthing).__module__.startswith('pages.'):
                page_class = getattr(module, smthing)
        if not page_class:
            modules.logging.warn('Subclass of Page is not found in <{}>', module_name)
            return None
        if page_class.__name__ not in self._executors:
            return page_class

    def loadpages(self):
        for module_name in os.listdir('pages'):
            if module_name.startswith('_'):
                continue
            try:
                module_name = os.path.splitext(module_name)[0]
                module = importlib.import_module('pages.{}'.format(module_name))
                page_class = self._search_module(module, module_name)
                if page_class:
                    self.add_page(page_class)
            except ImportError as e:
                modules.logging.error('Import error of <{}>: {}', module_name, e.args[0])


class Template:
    def __init__(self, name, login=False, **kwargs):
        self.name = name
        self._kwargs = kwargs
        if login:
            user_id = getuserid()
            self.add_parameter('user_id', user_id)
            self.add_parameter('loggedin', bool(user_id))
            self.add_parameter('adminlevel', getadminlevel())
            self.add_parameter('activated', activated())
            self.add_parameter('notifycount', get_notifycount(user_id))

    def add_parameter(self, name, value):
        self._kwargs[name] = value

    def template(self):
        return bottle.template(self.name, **self._kwargs)


controller = _PageController()


class PageBuilder:
    pass

