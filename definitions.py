import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEVELOP_CONFIG_PATH = os.path.join(ROOT_DIR, 'yaws/conf/develop.ini')
HOME_PATH = os.getenv('HOME')
YAWS_PATH = os.path.join(HOME_PATH, '.yaws')
USER_CONFIG_PATH = os.path.join(YAWS_PATH, 'config.ini')
USER_COOKIE_PATH = os.path.join(YAWS_PATH, 'cookie')
