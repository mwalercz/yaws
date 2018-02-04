import getpass
from ConfigParser import ConfigParser

import os
import shutil
import urllib3
from knot import Container

from definitions import USER_CONFIG_PATH, DEVELOP_CONFIG_PATH, YAWS_PATH, TEMPLATE_CONFIG_PATH
from yaws.dependencies import register


def make_app(
        config_path=USER_CONFIG_PATH,
        cli_username=None,
        password=None
):
    copy_config_to_user_dir_if_not_present()
    urllib3.disable_warnings()  # ssl warning about certs
    conf = ConfigParser()
    conf.read(config_path)
    conf = dict(conf.items('yaws'))
    usernames = (cli_username, conf.get('username'), getpass.getuser())
    conf.update(
        {
            'username': next(
                username for username in usernames
                if username is not None
            ),
            'password': password,
            'config_path': config_path,
        }
    )

    c = Container(conf=conf)
    register(c)
    return c


def copy_config_to_user_dir_if_not_present():
    if not os.path.isdir(YAWS_PATH):
        os.mkdir(YAWS_PATH, 0o700)
    if not os.path.isfile(USER_CONFIG_PATH):
        shutil.copyfile(src=TEMPLATE_CONFIG_PATH, dst=USER_CONFIG_PATH)
        os.chmod(USER_CONFIG_PATH, 0o700)


if __name__ == '__main__':
    container = make_app(
        config_path=DEVELOP_CONFIG_PATH,
        cli_username='admin',
        password='admin'
    )
    container('controller').request(
        method='GET',
        path='/works',
        params=[('status', 'UNKNOWN')]
    )
