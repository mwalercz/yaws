from definitions import USER_COOKIE_PATH
from yaws.authentication import Credentials, Authentication
from yaws.controller import Controller
from yaws.cookie_keeper import CookieKeeper
from yaws.requester import BrokerRequester
from yaws.user_switcher import UserSwitcher


def cookie_keeper(c):
    return CookieKeeper(
        cookie_path=USER_COOKIE_PATH
    )


def auth(c):
    return Authentication(
        cookie_keeper=c('cookie_keeper'),
    )


def requester(c):
    return BrokerRequester(
        url=c('conf')['url'],
        auth=c('auth'),
        cookie_keeper=c('cookie_keeper')
    )


def controller(c):
    return Controller(
        requester=c('requester'),
        url=c('conf')['url'],
        credentials=Credentials(c('conf')['username'], c('conf')['password']),
    )


def user_switcher(c):
    return UserSwitcher(
        config_path=c('conf')['config_path'],
        cookie_keeper=c('cookie_keeper'),
    )


def register(c):
    c.add_service(user_switcher)
    c.add_service(cookie_keeper)
    c.add_service(auth)
    c.add_service(requester)
    c.add_service(controller)
