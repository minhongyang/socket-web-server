import random
import time

import os

from jinja2 import FileSystemLoader, Environment


def log(*args, **kwargs):
    time_format = '<%Y/%m/%d %H:%M:%S>'
    value = time.localtime(int(time.time()))
    dt = time.strftime(time_format, value)
    print(dt, *args, **kwargs)


def random_string():
    seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 1)
        s += seed[random_index]
    return s


def formatted_time(unix_time):
    ft = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(unix_time))
    return ft


def configured_environment():
    path = '{}/views/'.format(os.path.dirname(__file__))
    loader = FileSystemLoader(path)
    return Environment(loader=loader)


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)


env = configured_environment()
