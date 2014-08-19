__author__ = 'sashgorokhov'
__email__ = 'sashgorokhov@gmail.com'

import datetime
import os
import time


def _time() -> str:
    return str(datetime.datetime.now())[:str(datetime.datetime.now()).find('.')]


_dir = 'logs'
_filename = _time().replace(':', '_') + '.log'
_filepath = os.path.join(_dir, _filename)

if not os.path.exists(_dir):
    os.mkdir(_dir)

_debug = False


def _writelog(msg:str):
    with open(_filepath, 'a') as f:
        f.write(msg + '\n')
    if debug:
        print(msg)


def debug(value):
    global _debug
    _debug = value
    _writelog('<<DEBUG ENABLED>>')


def write_formatted(type_:str, msg_:str, *args):
    _writelog('[{type_}] ({time_})\t{msg_}'.format(type_=type_, time_=_time(), msg_=msg_.format(*args)))


def info(msg, *args):
    write_formatted('INFO', msg, *args)


def warn(msg, *args):
    write_formatted('WARN', msg, *args)


def error(msg, *args):
    write_formatted('ERRO', msg, *args)


def logworktime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret_value = func(*args, **kwargs)
        elapsed = str(time.time() - start)
        info('Function <{}> runned {}s {}ms', func.__qualname__, *elapsed.split('.'))
        return ret_value

    return wrapper


def get_log() -> str:
    return open(_filepath, 'r').read()
