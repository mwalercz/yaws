import os

import shutil
from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install

from definitions import DEVELOP_CONFIG_PATH, YAWS_PATH, USER_CONFIG_PATH


def copy_config_to_user_dir_if_not_present():
    if not os.path.isdir(YAWS_PATH):
        os.mkdir(YAWS_PATH, 0o700)
    if not os.path.isfile(USER_CONFIG_PATH):
        shutil.copyfile(src=DEVELOP_CONFIG_PATH, dst=USER_CONFIG_PATH)
        os.chmod(USER_CONFIG_PATH, 0o700)


def path_in_project(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def read_file(filename):
    with open(path_in_project(filename)) as f:
        return f.read()


def read_reqs(filename):
    lines = read_file(filename).strip('\n')
    return lines.split('\n') if lines else []


class PostInstallCommand(install):
    def run(self):
        copy_config_to_user_dir_if_not_present()
        install.run(self)


setup(
    name="yaws",
    version="0.0.1",
    author="Maciej Walerczuk",
    author_email="mwalerczuk@gmail.com",
    description="yaws",
    license="BSD",
    packages=find_packages(include=path_in_project('yaws*'), exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'yaws = yaws.cli:yaws',
        ],
    },
    include_package_data=True,
    install_requires=read_reqs('requirements.txt'),
    tests_require=read_reqs('requirements_dev.txt'),
    zip_safe=False,
    cmdclass={
        'install': PostInstallCommand,
    },
)
