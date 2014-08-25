import json
import os
import random
import itertools
import traceback
import time

import bottle


config = json.load(open(os.path.join('modules', 'config.json'), 'r'))


def _generate_secret():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(10, 30)))


def extract_traceback(e):
    return '\n'.join(traceback.format_exception(e.__class__, e, e.__traceback__))


def generate_token():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(30, 40)))


config['secret'] = _generate_secret()


def exec_time_measure(callback):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        bottle.response.headers['X-Exec-Time'] = str(end - start)
        return body

    return wrapper
