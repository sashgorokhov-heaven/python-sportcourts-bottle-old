import datetime
import os, bottle
from modules import extract_traceback
import pages

_TRACEBACK_FILE = 'logs/traceback.txt'
_ACCESS_FILE = 'logs/access.txt'
_LOG_FILE = 'logs/log.txt'
DEBUG = False

if not os.path.exists('logs'):
    os.mkdir('logs')

def _check_size():
    for filename in [_ACCESS_FILE, _LOG_FILE]:
        if os.stat(filename).st_size>1024*1024:
            os.remove(filename)

def _write_line(filename:str, line:str):
    #_check_size()
    with open(filename, 'a') as f:
        f.write(line+'\n')
    if DEBUG:
        try:
            print(line)
        except Exception as e:
            try:
                print('Error while writing to console:', e.__class__.__name__)
            except:
                pass


def _get_access_line() -> str:
   line = bottle.request.remote_addr + ' "' + bottle.request.method + ' ' + bottle.request.fullpath
   if bottle.request.query_string:
       line += '?' + bottle.request.query_string
   line += '"'
   return line


def access_log(write:bool=True):
    if bottle.request.fullpath.startswith('/view') or bottle.request.fullpath.startswith('/images'):
        return
    line = _get_access_line()
    user_id = pages.auth_dispatcher.getuserid()
    if user_id:
        line += ' uid=[{}]'.format(user_id)
    time = str(datetime.datetime.now())
    format = '[{}] {} '.format(time, line)
    if write:
        _write_line(_ACCESS_FILE, format)
    return format

def error_log(e:Exception, message:str=None):
    line = access_log(True)
    if message:
        line += message + '- '
    line += e.__class__.__name__
    if len(e.args)>0:
        line += ': '+','.join(map(str, e.args))
    _write_line(_LOG_FILE, line)
    with open(_TRACEBACK_FILE, 'w') as f:
        f.write('\n'.join(extract_traceback(e)))