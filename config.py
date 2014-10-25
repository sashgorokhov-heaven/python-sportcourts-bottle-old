import random
import sys
import os
import itertools


sys.path.append('/bsp')

if not os.path.exists('/bsp/serverconfig.py'):
    raise FileNotFoundError('Config .py file is not found in /bsp folder!')

from serverconfig import *


def _generate_secret():
    return ''.join(
        random.sample(list(itertools.chain(map(chr, range(65, 91)), map(chr, range(97, 122)), map(str, range(1, 10)))),
                      random.randint(10, 30)))


if not debug:
    secret = _generate_secret()