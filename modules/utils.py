import pickle
import threading
from .myuwsgi import uwsgidecorators, uwsgi


def format_duration(duration:int) -> str:
    postfix = 'минут'
    prefix = int(str(duration)[-1])
    if prefix == 0 or 5 <= prefix <= 9 or 10<=duration<=19:
        postfix = 'минут'
    elif prefix == 1:
        postfix = 'минута'
    elif 2 <= prefix <= 4:
        postfix = 'минуты'
    if duration > 60:
        duration = round(duration / 60)
        prefix = int(str(duration)[-1])
        if prefix == 0 or 5 <= prefix <= 9 or 10<=duration<=19:
            postfix = 'часов'
        elif prefix == 1:
            postfix = 'час'
        elif 2 <= prefix <= 4:
            postfix = 'часа'
    return str(duration) + ' ' + postfix


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=func.__qualname__)
        thread.start()
        return thread

    return wrapper


_spoolers = dict() # func key -> func
logfunc = lambda text, error: str(text)+str(error)

@uwsgidecorators.spool
def _spool_dispatcher(*args, **kwargs):
    try:
        data = args[0]
        spool_key = data['spool_key']
        if spool_key not in _spoolers:
            try:
                raise KeyError('Spooler for <{}> not found'.format(spool_key))
            except KeyError as e:
                logfunc(e.args[0], e)
                return uwsgi.SPOOL_OK
        args, kwargs = data['data']
        try:
            retval = _spoolers[spool_key](*args, **kwargs)
        except Exception as e:
            logfunc('Error while executong spool function <{}> on key <{}>'.format(_spoolers[spool_key].__name__,
                                                                                           spool_key), e)
            return uwsgi.SPOOL_OK
        if not retval:
            return uwsgi.SPOOL_OK
        return retval
    except Exception as e:
        logfunc('Error processing spooler', e)
        return uwsgi.SPOOL_OK


def spool(spool_key:str):
    def decorator(func):
        _spoolers[spool_key] = func
        def wrapper(*args, **kwargs):
            pickleddata = pickle.dumps((args, kwargs))
            _spool_dispatcher.spool(spool_key=spool_key, data=pickleddata)
        setattr(wrapper, 'pure', func)
        return wrapper
    return decorator

def spool_func(func, *args, **kwargs):
    return func(*args, **kwargs)
    #spool(func.__name__)(func)(*args, **kwargs)