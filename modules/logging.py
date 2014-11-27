import base64
import datetime

import bottle

import dbutils
import modules
from modules import utils
import pages
from modules.myuwsgi import uwsgi


@utils.spool('logs')
def _writedb(**kwargs):
    try:
        with dbutils.dbopen(**dbutils.logsdb_connection) as db:
            keys = list(kwargs.keys())
            if 'traceback' in kwargs:
                kwargs['traceback'] = base64.b64encode(kwargs['traceback'].encode()).decode()
            if 'error' in kwargs:
                kwargs['error'] = kwargs['error'].replace('"', '').replace("'", '')
            if 'error_description' in kwargs:
                kwargs['error_description'] = kwargs['error_description'].replace('"', '').replace("'", '')
            values = [kwargs[i] for i in keys]
            db.execute(
                "INSERT INTO access (" + ", ".join(keys) + ") VALUES (" + ','.join(
                    list(map(lambda x: "'{}'".format(x), values))) + ")"
            )

    except Exception as e:
        try:
            print(e)
        except:
            pass
        return uwsgi.SPOOL_OK
        # return uwsgi.SPOOL_RETRY TODO
    return uwsgi.SPOOL_OK


def _send(data:dict):
    _writedb(**data)


def _access_data(time:float=0.0) -> dict:
    data = dict()
    data['ip'] = bottle.request.remote_addr
    data['httpmethod'] = bottle.request.method
    data['path'] = bottle.request.fullpath + ('?' + bottle.request.query_string if bottle.request.query_string else '')
    data['user_id'] = pages.auth.current().user_id()
    data['useragent'] = bottle.request.get_header('User-Agent', '')
    data['time'] = time
    data['referer'] = bottle.request.get_header('Referer')
    data['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data


def _error_data(error:Exception, time:float=0.0) -> dict():
    data = _access_data(time)
    data['error'] = error.__class__.__name__
    if len(error.args) > 0:
        data['error_description'] = ','.join(map(str, error.args))
    data['traceback'] = modules.extract_traceback(error)
    return data


def access(time:float=0.0):
    if bottle.request.fullpath.startswith('/view') or bottle.request.fullpath.startswith('/images'):
        return
    data = _access_data(time)
    _send(data)


def error(e:Exception, time:float=0.0):
    data = _error_data(e)
    _send(data)


@utils.spool('error_message')
def message(msg:str, e:Exception):
    with dbutils.dbopen(**dbutils.logsdb_connection) as db:
        error = e.__class__.__name__.replace('"', '').replace("'", '')
        error_description = ','.join(map(str, error.args)).replace('"', '').replace("'", '')
        traceback = base64.b64encode(modules.extract_traceback(e).encode()).decode()
        db.execute("INSERT INTO logsdb.messages (message, error, error_description, traceback) VALUES ('{}', '{}', '{}', '{}')".format(msg, error, error_description, traceback))
        return uwsgi.SPOOL_OK