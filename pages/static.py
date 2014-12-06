import bottle
import os
import config
import hashlib

@bottle.get('/view/<path:path>')
def static(path:str):
    filename = os.path.join(config.paths.server.static, path)
    resp = bottle.static_file(path, config.paths.server.static)
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            hash = hashlib.sha224(f.read()).hexdigest()
        resp.add_header('ETag', hash)
        resp.add_header('Cache-Control', 'max-age={}'.format(604800))
    return resp