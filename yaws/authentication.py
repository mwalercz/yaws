from requests.auth import HTTPBasicAuth

from yaws.exceptions import NoCookieException


class Authentication(object):
    def __init__(self, cookie_keeper, credentials):
        self.cookie_keeper = cookie_keeper
        self.credentials = credentials

    def add_headers(self, request):
        if self.credentials.are_correct():
            request.auth = HTTPBasicAuth(
                self.credentials.username,
                self.credentials.password
            )
            return
        cookie = self.cookie_keeper.get_cookie()
        if not cookie:
            raise NoCookieException()

        request.cookies = {'YAWSM_SESSION': cookie}


class Credentials(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def are_correct(self):
        return self.password and self.username

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
        }
