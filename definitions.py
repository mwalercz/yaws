import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEVELOP_CONFIG_PATH = os.path.join(ROOT_DIR, 'yaws/conf/develop.cfg')
TEMPLATE_CONFIG_PATH = os.path.join(ROOT_DIR, 'yaws/conf/template.cfg')
HOME_PATH = os.getenv('HOME')
YAWS_PATH = os.path.join(HOME_PATH, '.yaws')
USER_CONFIG_PATH = os.path.join(YAWS_PATH, 'config.cfg')
USER_COOKIE_PATH = os.path.join(YAWS_PATH, 'cookie')
