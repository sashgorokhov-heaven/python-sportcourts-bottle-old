_ipbase = 'ipbase.json'
import bottle


def skip(ip:str, fullpath:str):
    if fullpath.startswith('/view') or fullpath.startswith('/images'):
        return True
    return True


def ipfilter(func):
    def wrapper(*args, **kwargs):
        if not skip(bottle.request.remote_addr, bottle.request.fullpath):
            raise bottle.HTTPError(403, 'Your IP ({}) was banned. Please contact domain administrator for more details.'.format(bottle.request.remote_addr))
        return func(*args, **kwargs)

    return wrapper