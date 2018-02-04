from requests.auth import HTTPBasicAuth

from yaws.exceptions import NoCredentialsException


class Authentication(object):
    def __init__(self, cookie_keeper):
        self.cookie_keeper = cookie_keeper

    def get_headers(self, credentials):
        if credentials.seems_correct():
            return {
                'auth': HTTPBasicAuth(
                    credentials.username,
                    credentials.password
                )
            }
        cookie = self.cookie_keeper.get_cookie()
        if not cookie:
            raise NoCredentialsException()

        return {'cookies': {'YAWSM_SESSION': cookie}}


class Credentials(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def seems_correct(self):
        return self.password and self.username

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
        }
