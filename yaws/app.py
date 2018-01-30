import logging
import os

import shutil
import urllib3
from knot import Container

from definitions import USER_CONFIG_PATH, YAWS_PATH, DEVELOP_CONFIG_PATH
from yaws.dependencies import register


def init_app(
        username,
        password,
):
    return make_app(
        config_path=USER_CONFIG_PATH,
        username=username,
        password=password,
    )


def make_app(
        config_path=DEVELOP_CONFIG_PATH,
        username=None,
        password=None
):
    logging.basicConfig(
        level=logging.INFO,
    )
    urllib3.disable_warnings()  # ssl warning about certs
    c = Container(dict(
        config_path=config_path,
        username=username,
        password=password,
    ))
    register(c)
    c('controller')
    return c


if __name__ == '__main__':
    container = make_app(username='admin', password='admin')
    container('controller').request(
        method='GET',
        path='/works',
        params=[('status', 'unknown')]
    )
