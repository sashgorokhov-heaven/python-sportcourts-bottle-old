import json
import os
import random
import itertools
import traceback
import time

import bottle


TEST = False

if not TEST:
    config = json.load(open(os.path.join('modules', 'config.json'), 'r'))
else:
    config = json.load(open(os.path.join('modules', 'testconfig.json'), 'r'))

config['testing'] = TEST


def pager(page, count:int=8) -> tuple:
    """
    page:int starts from 1 - 1,2,3...
    count - items per page

    :return offset, count (ready to use in LIMIT)
    """
    page -= 1
    return page * count, count


def _generate_secret():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(10, 30)))


def extract_traceback(e, sep:str='\n'):
    return sep.join(traceback.format_exception(e.__class__, e, e.__traceback__))


def generate_token():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(30, 40)))


config['secret'] = config['debug_secret'] if config['debug'] else _generate_secret()


class create_link:
    @staticmethod
    def game(game:dict) -> str:
        link = "<a href=\"/games?game_id={}\">#{} | {}</a>".format(game['game_id'], game['game_id'],
                                                                   game['description'])
        return link


    @staticmethod
    def user(user:dict) -> str:
        link = "<a href=\"/profile?user_id={}\">{} {}</a>".format(user['user_id'], user['first_name'],
                                                                  user['last_name'])
        return link


def exec_time_measure(callback):
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        bottle.response.headers['X-Exec-Time'] = str(end - start)
        return body

    return wrapper
