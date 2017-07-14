from ConfigParser import ConfigParser

from dq_cli.authentication import Credentials, Authentication
from dq_cli.cookie_keeper import CookieKeeper
from dq_cli.requester import Requester


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def credentials(c):
    return Credentials(c('username'), c('password'))


def cookie_keeper(c):
    return CookieKeeper(
        secret_folder=c('conf').get('other', 'secret_folder'),
        cookie_filename=c('conf').get('other', 'cookie_filename'),
    )


def auth(c):
    return Authentication(
        cookie_keeper=c('cookie_keeper'),
        credentials=c('credentials')
    )


def requester(c):
    return Requester(
        base_url=c('conf').get('broker', 'url'),
        auth=c('auth'),
        cookie_keeper=c('cookie_keeper')
    )


def register(c):
    c.add_service(conf)

    c.add_service(credentials)
    c.add_service(cookie_keeper)
    c.add_service(auth)
    c.add_service(requester)
