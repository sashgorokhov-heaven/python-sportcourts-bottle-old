import base64
import bottle
import modules
from modules import dbutils, utils
import pages
import uwsgi


@utils.spooler
def _writedb(ip:str, path:str, httpmethod:str='GET', referer:str='None', user_id:int=0, message:str=None,
             error:str=None, error_description:str=None, traceback:str=None):
    try:
        with dbutils.dbopen(host=modules.config['logdb']['dbhost'],
                            user=modules.config['logdb']['dbuser'],
                            passwd=modules.config['logdb']['dbpasswd'],
                            db=modules.config['logdb']['dbname'],
                            charset='utf8') as db:
            db.execute(
                'INSERT INTO access (ip, path, httpmethod, referer, user_id, message, error, error_description, traceback) VALUES ("{}", "{}", "{}", "{}", {}, {}, {}, {}, {})'.format(
                    ip, path, httpmethod, referer, user_id,
                    '"{}"'.format(message) if message else 'NULL',
                    '"{}"'.format(error) if error else 'NULL',
                    '"{}"'.format(error_description) if error_description else 'NULL',
                    '"{}"'.format(base64.b64encode(traceback).decode()) if traceback else 'NULL'))
    except Exception as e:
        print(e)
        return uwsgi.SPOOL_RETRY
    return uwsgi.SPOOL_OK


def _send(data:dict):
    _writedb.spool(**data)


def _access_data() -> dict:
    data = dict()
    data['ip'] = bottle.request.remote_addr
    data['httpmethod'] = bottle.request.method
    data['path'] = bottle.request.fullpath + ('?' + bottle.request.query_string if bottle.request.query_string else '')
    data['user_id'] = pages.auth_dispatcher.getuserid()
    data['referer'] = bottle.request.get_header('Referer')
    return data


def _error_data(error:Exception) -> dict():
    data = _access_data()
    data['error'] = error.__class__.__name__
    if len(error.args) > 0:
        data['error_description'] = ','.join(map(str, error.args))
    data['traceback'] = modules.extract_traceback(error)
    return data


def access():
    if bottle.request.fullpath.startswith('/view') or bottle.request.fullpath.startswith('/images'):
        return
    data = _access_data()
    _send(data)


def error(e:Exception):
    data = _error_data(e)
    _send(data)