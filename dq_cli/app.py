import logging
import os

import shutil
import urllib3
from knot import Container

from definitions import USER_CONFIG_PATH, USER_DQ_CLI_PATH, DEVELOP_CONFIG_PATH
from dq_cli.dependencies import register


def init_app(
        username,
        password,
):
    copy_config_to_user_dir_if_not_present()
    return make_app(
        config_path=USER_CONFIG_PATH,
        username=username,
        password=password,
    )


def make_app(
        config_path=DEVELOP_CONFIG_PATH,
        username='test',
        password='test'
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


def copy_config_to_user_dir_if_not_present():
    if not os.path.isdir(USER_DQ_CLI_PATH):
        os.mkdir(USER_DQ_CLI_PATH, 0o700)
    if not os.path.isfile(USER_CONFIG_PATH):
        shutil.copyfile(src=DEVELOP_CONFIG_PATH, dst=USER_CONFIG_PATH)
        os.chmod(USER_CONFIG_PATH, 0o700)


if __name__ == '__main__':
    container = make_app()
    container('controller').request(
        method='POST',
        path='/users/test/works',
        json={
            'command': 'ls',
            'cwd': '/home/test',
        },
    )
