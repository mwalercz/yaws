import os


class CookieKeeper(object):
    def __init__(self, cookie_path):
        self.cookie_path = cookie_path

    def save_cookie(self, cookie):
        with open(self.cookie_path, mode='w') as f:
            f.write(cookie)

    def get_cookie(self):
        if not os.path.isfile(self.cookie_path):
            return None
        with open(self.cookie_path, mode='r') as f:
            return f.readline().strip()
