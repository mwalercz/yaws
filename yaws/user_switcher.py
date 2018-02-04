from ConfigParser import ConfigParser


class UserSwitcher:
    def __init__(self, config_path, cookie_keeper):
        self.config_path = config_path
        self.cookie_keeper = cookie_keeper

    def switch(self, username):
        parser = ConfigParser()
        parser.read(self.config_path)
        parser.set('yaws', 'username', username)
        with open(self.config_path, 'w+') as f:
            parser.write(f)

        self.cookie_keeper.remove_cookie()
