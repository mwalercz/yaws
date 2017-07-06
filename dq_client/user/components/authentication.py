from dq_client.user.components.cookie_keeper import CookieKeeper
from dq_client.user.exceptions import NoCookieException


class Authentication(object):
    def __init__(self, cookie_keeper: CookieKeeper, parent_pid):
        self.cookie_keeper = cookie_keeper
        self.parent_pid = parent_pid

    def get_headers(self, credentials):
        if credentials.are_correct():
            return credentials.to_dict()
        else:
            cookie = self.cookie_keeper.get_cookie()
            if cookie:
                return {
                    'x-cookie': cookie,
                    'x-parent-pid': self.parent_pid,
                }
            else:
                raise NoCookieException()


class Credentials(object):
    def __init__(self, username, password, parent_pid):
        self.username = username
        self.password = password
        self.parent_pid = parent_pid

    def are_correct(self):
        return self.password and self.username

    def to_dict(self):
        return dict(
            username=self.username,
            password=self.password,
            parent_pid=self.parent_pid,
        )
