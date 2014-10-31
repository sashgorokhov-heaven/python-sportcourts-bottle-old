import config

try:
    import uwsgi as _uwsgi
    import uwsgidecorators as _uwsgidecorators
except ImportError:
    import_error = True
    if not config.standalone:
        try:
            print('UWSGI import error')
        except IOError:
            pass
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
        pass

    @staticmethod
    def filemon(*args):
        pass


uwsgi = _my_uwsgi if import_error or config.standalone else _uwsgi
uwsgidecorators = _my_uwsgidecorators if import_error or config.standalone else _uwsgidecorators