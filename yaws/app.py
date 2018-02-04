import getpass
import logging
from ConfigParser import ConfigParser


import urllib3
from knot import Container

from definitions import USER_CONFIG_PATH, DEVELOP_CONFIG_PATH
from yaws.dependencies import register


def make_app(
        config_path=USER_CONFIG_PATH,
        cli_username=None,
        cli_password=None
):
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
            'password': cli_password
        }
    )

    c = Container(conf=conf)
    register(c)
    return c


if __name__ == '__main__':
    container = make_app(
        config_path=DEVELOP_CONFIG_PATH,
        username='admin',
        password='admin'
    )
    container('controller').request(
        method='GET',
        path='/works',
        params=[('status', 'unknown')]
    )
