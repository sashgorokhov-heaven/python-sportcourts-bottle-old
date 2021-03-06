import config

try:
    import uwsgi as _uwsgi
    import uwsgidecorators as _uwsgidecorators
except ImportError:
    import_error = True
    if not config.standalone:
        raise
else:
    import_error = False


class _my_uwsgi:
    SPOOL_OK = _uwsgi.SPOOL_OK if not import_error and not config.standalone else 0
    SPOOL_RETRY = _uwsgi.SPOOL_RETRY if not import_error and not config.standalone else 0
    spooler = None

    @staticmethod
    def spool(*args, **kwargs):
        pass

    @staticmethod
    def reload():
        pass



class _my_uwsgidecorators:
    @staticmethod
    def cron(*args):
        def wrapper(*args, **kwargs):
            pass
        return wrapper

    @staticmethod
    def filemon(*args):
        def wrapper(*args, **kwargs):
            pass
        return wrapper

    @staticmethod
    def timer(*args, **kwargs):
        def wrapper(*args, **kwargs):
            pass
        return wrapper

    @staticmethod
    def spool(func):
        return func


uwsgi = _my_uwsgi if import_error or config.standalone else _uwsgi
uwsgidecorators = _my_uwsgidecorators if import_error or config.standalone else _uwsgidecorators