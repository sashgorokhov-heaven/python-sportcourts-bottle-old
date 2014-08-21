import importlib
import os

import bottle

import modules
import modules.logging


def getuserid():
    return int(bottle.request.get_cookie('user_id', 0, modules.config['secret']))


def getadminlevel():
    return int(bottle.request.get_cookie('adminlevel', 0, modules.config['secret']))


def loggedin():
    return bool(getuserid())


def activated():
    return bool(int(bottle.request.get_cookie('activated', 0, modules.config['secret'])))


def setlogin(func):
    def wrapper(*args, **kwargs):
        template = func(*args, **kwargs)
        user_id = getuserid()
        template.add_parameter('user_id', user_id)
        template.add_parameter('loggedin', bool(user_id))
        template.add_parameter('adminlevel', getadminlevel())
        return template

    return wrapper


def handleerrors(template_name):
    def decor(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (bottle.HTTPResponse, bottle.HTTPError) as e:
                modules.logging.warn('Bottle error {}: {}'.format(e.__class__.__name__, e.args))
                raise e
            except Exception as e:
                modules.logging.error(e.__class__.__name__ + ': {}', e.args[0] if len(e.args) > 0 else '')
                modules.logging.info(modules.extract_traceback(e))
                return Template(template_name, error=e.__class__.__name__,
                                error_description=e.args[0] if len(e.args) > 0 else '',
                                traceback=modules.extract_traceback(e), login=True)

        return wrapper

    return decor


class Page:
    path = ['']  # index

    def execute(self, method:str):
        if method == 'GET': return self.get().template()
        if method == 'POST': return self.post().template()

    def get(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class PageController:
    def __init__(self):
        self._pages = dict()
        self.loadpages()

    def loadpages(self):
        bottle.TEMPLATES.clear()
        self._pages.clear()
        for module_name in os.listdir('pages'):
            if module_name.startswith('_'):
                continue
            try:
                module_name = os.path.splitext(module_name)[0]
                module = importlib.import_module('pages.{}'.format(module_name))
                module = importlib.reload(module)
                pages_class = None
                for smthing in dir(module):
                    if not smthing.startswith('_') \
                            and type(getattr(module, smthing)) == type(Page) \
                            and issubclass(getattr(module, smthing), Page) \
                            and getattr(module, smthing).__module__.startswith('pages.'):
                        pages_class = getattr(module, smthing)
                if not pages_class:
                    modules.logging.error('Subclass of Page is not found in <{}>', module_name)
                    continue
                instance = pages_class()
                for path in instance.path:
                    if path in self._pages:
                        modules.logging.warn('Path conflict <{}: ({})> with <{}>'.format(
                            pages_class.__name__, path, self._pages[path].__class__.__name__))
                        continue
                    self._pages[path] = instance
            except ImportError as e:
                modules.logging.error('Import error of <{}>: {}', module_name, e.args[0])

    def execute(self, method:str, path:str):
        if path in self._pages:
            try:
                return self._pages[path].execute(method)
            except (bottle.HTTPResponse, bottle.HTTPError) as e:
                modules.logging.warn('Bottle error {}: {}'.format(e.__class__.__name__, e.args))
                raise e
            except Exception as e:
                modules.logging.error(path + ' | ' + e.__class__.__name__ + ': {}',
                                      e.args[0] if len(e.args) > 0 else '')
                modules.logging.info(modules.extract_traceback(e))
                return bottle.template('404', error=e.__class__.__name__,
                                       error_description=e.args[0] if len(e.args) > 0 else '',
                                       traceback=modules.extract_traceback(e),
                                       login=True)
        if os.path.exists(os.path.join(modules.config['server_root'], 'static', path)):
            return bottle.static_file(path, os.path.join(modules.config['server_root'], 'static'))
        raise bottle.HTTPError(404)


class Template:
    def __init__(self, name, login=False, **kwargs):
        self.name = name
        self._kwargs = kwargs
        if login:
            user_id = int(bottle.request.get_cookie('user_id', 0, modules.config['secret']))
            self.add_parameter('user_id', user_id)
            self.add_parameter('loggedin', bool(user_id))

    def add_parameter(self, name, value):
        self._kwargs[name] = value

    def template(self):
        return bottle.template(self.name, **self._kwargs)


controller = PageController()

