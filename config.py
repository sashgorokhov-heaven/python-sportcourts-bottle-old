import random
import sys
import os
import itertools

configpath = '/Users/vitaliyharchenko/SportCourts' # сюда путь до конфига

sys.path.append(configpath)

if not os.path.exists(os.path.join(configpath, 'serverconfig.py')):
    raise FileNotFoundError('Config .py file is not found in {} folder!'.format(configpath))

from serverconfig import *


_notfound = list()
for class_name in filter(lambda x: not x.startswith('_'), paths.__dict__):
    class_type = getattr(paths, class_name)
    for pathattr in filter(lambda x: not x.startswith('_'), class_type.__dict__):
        path = getattr(class_type, pathattr)
        if isinstance(path, str):
            path = [path]
        for p in path:
            if not os.path.exists(p):
                _notfound.append(('paths.{}.{}'.format(class_name, pathattr), p))
if len(_notfound)>0:
    for path in _notfound:
        try:
            print('{} = "{}" Not found!'.format(*path))
        except:
            raise FileNotFoundError(path[1])


def _generate_secret():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(10, 30)))


if not debug:
    secret = _generate_secret()

