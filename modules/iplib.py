_ipbase = 'ipbase.json'
import bottle

def skip(ip:str, fullpath:str):
    if fullpath.startswith('/view') or fullpath.startswith('/images'):
        return True
    return True


def ipfilter(func):
    def wrapper(*args, **kwargs):
        if not skip(bottle.request.remote_addr, bottle.request.fullpath):
            raise bottle.HTTPError(404)
        return func(*args, **kwargs)
    return wrapper