import os

from setuptools import find_packages
from setuptools import setup


def path_in_project(*path):
    return os.path.join(os.path.dirname(__file__), *path)


def read_file(filename):
    with open(path_in_project(filename)) as f:
        return f.read()


def read_reqs(filename):
    lines = read_file(filename).strip('\n')
    return lines.split('\n') if lines else []

setup(
    name="dq_cli",
    version="0.0.1",
    author="Maciej Walerczuk",
    author_email="mwalerczuk@gmail.com",
    description="dq_cli",
    license="BSD",
    packages=find_packages(include=path_in_project('dq_cli*'), exclude=['tests*']),
    entry_points={
        'console_scripts': [
            'yaws = dq_cli.cli:queue',
        ],
    },
    include_package_data=True,
    install_requires=read_reqs('requirements.txt'),
    tests_require=read_reqs('requirements_dev.txt'),
    zip_safe=False,
)
