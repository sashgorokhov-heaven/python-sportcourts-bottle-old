import threading, pickle
import uwsgi

def format_duration(duration:int) -> str:
    postfix = 'минут'
    prefix = int(str(duration)[-1])
    if prefix == 0 or 5 <= prefix <= 9:
        postfix = 'минут'
    elif prefix == 1:
        postfix = 'минута'
    elif 2 <= prefix <= 4:
        postfix = 'минуты'
    if duration > 60:
        duration = round(duration / 60)
        prefix = int(str(duration)[-1])
        if prefix == 0 or 5 <= prefix <= 9:
            postfix = 'часов'
        elif prefix == 1:
            postfix = 'час'
        elif 2 <= prefix <= 4:
            postfix = 'часа'
        if duration > 24:
            duration = round(duration / 24)
            prefix = int(str(duration)[-1])
            if prefix == 0 or 5 <= prefix <= 9:
                postfix = 'дней'
            elif prefix == 1:
                postfix = 'день'
            elif 2 <= prefix <= 4:
                postfix = 'дня'
    return str(duration)+' '+postfix


def threaded(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs, name=func.__qualname__)
        thread.start()
        return thread

    return wrapper


#_spoolers = dict() # func key -> func
#
#
#def _spool_dispatcher(data:dict):
#    spool_key = data[b'key'].decode()
#    pickleddata = pickle.loads(data[b'data'])
#    args, kwargs = pickleddata
#    retval = _spoolers[spool_key](*args, **kwargs)
#    if not retval:
#        return uwsgi.SPOOL_OK
#    return retval


def spooler(spool_key:str):
    def wraper(func):
        #def spool(*args, **kwargs):
        #    pickleddata = pickle.dumps((args, kwargs))
        #    uwsgi.spool({b'data': pickleddata, b'key':spool_key.encode()})
        #_spoolers[spool_key] = func
        #uwsgi.spooler = _spool_dispatcher
        #setattr(func, 'spool', spool)
        return func
    return wraper

def as_spooler(func):
    def wrapper(*args, **kwargs):
        #func.spool(*args, **kwargs)
        return func(*args, **kwargs)
    return wrapper