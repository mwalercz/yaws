from ConfigParser import ConfigParser

from definitions import USER_COOKIE_PATH
from dq_cli.authentication import Credentials, Authentication
from dq_cli.controller import Controller
from dq_cli.cookie_keeper import CookieKeeper
from dq_cli.requester import BrokerRequester


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def broker_url(c):
    return c('conf').get('broker', 'url')


def credentials(c):
    return Credentials(c('username'), c('password'))


def cookie_keeper(c):
    return CookieKeeper(
        cookie_path=USER_COOKIE_PATH
    )


def auth(c):
    return Authentication(
        cookie_keeper=c('cookie_keeper'),
        credentials=c('credentials')
    )


def requester(c):
    return BrokerRequester(
        broker_url=c('broker_url'),
        auth=c('auth'),
        cookie_keeper=c('cookie_keeper')
    )


def controller(c):
    return Controller(
        requester=c('requester'),
        url=c('broker_url'),
    )


def register(c):
    c.add_service(conf)
    c.add_service(broker_url)

    c.add_service(credentials)
    c.add_service(cookie_keeper)
    c.add_service(auth)
    c.add_service(requester)
    c.add_service(controller)
