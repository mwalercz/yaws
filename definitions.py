import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEVELOP_CONFIG_PATH = os.path.join(ROOT_DIR, 'dq_cli/conf/develop.ini')
HOME_PATH = os.getenv('HOME')
USER_QUEUE_PATH = os.path.join(HOME_PATH, '.queue')
USER_CONFIG_PATH = os.path.join(USER_QUEUE_PATH, 'config.ini')
USER_COOKIE_PATH = os.path.join(USER_QUEUE_PATH, 'cookie')
