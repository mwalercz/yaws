from ConfigParser import ConfigParser

from definitions import USER_COOKIE_PATH
from yaws.authentication import Credentials, Authentication
from yaws.controller import Controller
from yaws.cookie_keeper import CookieKeeper
from yaws.requester import BrokerRequester


def broker_url(c):
    return c('conf')['url']


def credentials(c):
    return Credentials(c('conf')['username'], c('conf')['password'])


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
    c.add_service(broker_url)

    c.add_service(credentials)
    c.add_service(cookie_keeper)
    c.add_service(auth)
    c.add_service(requester)
    c.add_service(controller)
