import getpass
from json import dumps

import click
from requests import ConnectionError
from requests import HTTPError
from requests import RequestException

from yaws.exceptions import NoCredentialsException


class AuthFailedException(Exception):
    pass


class Controller:
    def __init__(self, requester, url, credentials):
        self.credentials = credentials
        self.requester = requester
        self.url = url

    def request(self, method, path, json=None, params=None, iterator=0):
        if iterator >= 2:
            return
        try:
            self._request(method, path, json, params, self.credentials)
        except (AuthFailedException, NoCredentialsException):
            click.echo(
                'Please provide correct password.'
            )
            self.credentials.password = getpass.unix_getpass()
            self.request(method, path, json, params, iterator + 1)

    def _request(self, method, path, json=None, params=None, credentials=None):
        try:
            response = self.requester.make_request(method, path, json, params, credentials)
            click.echo(dumps(response.json(), indent=4, sort_keys=True))
        except HTTPError as exc:
            if exc.response.status_code == 401:
                raise AuthFailedException()
            elif exc.response.status_code == 403:
                click.echo(
                    'You don\'t have access to this resource.'
                )
            else:
                self._handle_unknown_error(exc)
        except ConnectionError as exc:
            click.echo(
                'Server: "{}" is unavailable. '
                'Try again later. Maybe url is wrong?'.format(self.url)
            )
        except RequestException as exc:
            self._handle_unknown_error(exc)

    def _handle_unknown_error(self, exc):
        click.echo('Something went wrong')
        click.echo(exc.response.status_code)
        click.echo(exc.response.text)
