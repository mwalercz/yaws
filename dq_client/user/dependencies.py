import asyncio
from configparser import ConfigParser

import os

from dq_client.user.components.authentication import Credentials, Authentication
from dq_client.user.components.cookie_keeper import CookieKeeper
from dq_client.user.components.factory import UserFactory
from dq_client.user.components.protocol import UserProtocol
from dq_client.user.components.serializers import JsonSerializer, JsonDeserializer


def conf(c):
    conf = ConfigParser()
    conf.read(c('config_path'))
    return conf


def serializer(c):
    return JsonSerializer()


def deserializer(c):
    return JsonDeserializer()


def credentials(c):
    return Credentials(c('username'), c('password'), os.getppid())


def cookie_keeper(c):
    return CookieKeeper(
        secret_folder=c('conf')['other']['secret_folder'],
        cookie_filename=c('conf')['other']['cookie_filename'],
    )


def auth(c):
    return Authentication(c('cookie_keeper'), os.getppid())


def factory(c):
    factory = UserFactory(
        master_wss_uri=c('conf')['master']['wss_uri'],
        headers=c('auth').get_headers(c('credentials'))
    )
    factory.protocol = c('protocol')
    return factory


def loop(c):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    return loop


def protocol(c):
    protocol = UserProtocol
    protocol.cookie_keeper = c('cookie_keeper')
    protocol.loop = c('loop')
    protocol.serializer = c('serializer')
    protocol.deserializer = c('deserializer')
    return protocol


def register(c):
    c.add_service(conf)
    c.add_service(serializer)
    c.add_service(deserializer)
    c.add_service(credentials)
    c.add_service(cookie_keeper)
    c.add_service(auth)
    c.add_service(factory)
    c.add_service(protocol)
    c.add_service(loop)
