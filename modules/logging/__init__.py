import socket, bottle, pages, modules
from modules.logging import speaker
import uwsgi

def _send_(data:dict):
    data = _decode_data(data)
    data['user_id'] = int(data['user_id'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    addr = (modules.config['log_server']['ip'], int(modules.config['log_server']['port']))
    try:
        sock.connect(addr)
        session = speaker.Session(sock, addr)
        session.send(modules.config['log_server']['passwd'])
        if session.recieve()['status'] == 1:
            return session.close()
        session.send({'data': data})
    except:
        return uwsgi.SPOOL_RETRY
    finally:
        try:
            sock.close()
        except:
            pass
    return uwsgi.SPOOL_OK


def _encode_data(data:dict) -> dict:
    data = dict(zip(map(lambda x: x.encode(), data), map(lambda x: str(data[x]).encode(), data)))
    return data


def _decode_data(data:dict) -> dict:
    data.pop('spooler_task_name')
    data = dict(zip(map(lambda x: x.decode(), data), map(lambda x: data[x].decode(), data)))
    return data


def _send(data:dict):
    uwsgi.spool(_encode_data(data), spooler='/bsp/spool_log')


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


def error(error:Exception):
    data = _error_data(error)
    _send(data)


uwsgi.spooler = _send_