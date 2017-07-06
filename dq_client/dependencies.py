import os
from ConfigParser import ConfigParser

import trollius
from dq_client.ws.factory import UserFactory

from dq_client.services.authentication import Credentials, Authentication
from dq_client.services.cookie_keeper import CookieKeeper
from dq_client.services.serializers import JsonSerializer, JsonDeserializer
from dq_client.ws.protocol import UserProtocol


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
        secret_folder=c('conf').get('other', 'secret_folder'),
        cookie_filename=c('conf').get('other', 'cookie_filename'),
    )


def auth(c):
    return Authentication(c('cookie_keeper'), os.getppid())


def factory(c):
    factory = UserFactory(
        broker_wss_uri=c('conf').get('broker', 'wss_uri'),
        headers=c('auth').get_headers(c('credentials'))
    )
    factory.protocol = c('protocol')
    return factory


def loop(c):
    loop = trollius.get_event_loop()
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
