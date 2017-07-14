import logging
from json import dumps

import click
from knot import Container
from requests import ConnectionError
from requests import HTTPError
from requests import RequestException
import urllib3

from dq_cli.dependencies import register


def make_app(
        config_path='conf/develop.ini',
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
    return UserApp(
        requester=c('requester'),
        username=c('username'),
        url=c('conf').get('broker', 'url'),
    )


class UserApp:
    def __init__(self, requester, username, url):
        self.requester = requester
        self.url = url
        self.username = username

    def request(self, method, path, json=None, params=None):
        try:
            response = self.requester.request(method, path, json, params)
            click.echo(dumps(response.json(), indent=4, sort_keys=True))
        except HTTPError as exc:
            if exc.response.status_code == 401:
                click.echo(
                    'Wrong username/password or cookie is too old. '
                    'Use --login option.'
                )
            elif exc.response.status_code == 403:
                click.echo(
                    'You don\'t have access to this resource.'
                )
            else:
                self._handle_unknown_error(exc)
        except ConnectionError as exc:
            click.echo(
                'Server: "{}" is unavailable. Try again later. Maybe url is wrong?'.format(self.url)
            )
        except RequestException as exc:
            self._handle_unknown_error(exc)

    def _handle_unknown_error(self, exc):
        click.echo('Something went wrong')
        click.echo(exc.response.status_code)
        click.echo(exc.response.text)


if __name__ == '__main__':
    app = make_app()
    app.request(
        method='POST',
        path='/users/test/works',
        json={
            'command': 'ls',
            'cwd': '/home/test',
        },
    )
