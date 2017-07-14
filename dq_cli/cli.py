import getpass
import os
import sys

import click
from click import pass_context
from click import prompt
from dq_cli.user_app import make_app

from dq_cli.exceptions import NoCookieException


@click.group()
@click.option(
    '-c', '--config',
    default=os.path.join(os.getenv("HOME") + '.dist_queue/develop.ini'),
    type=click.Path(exists=True),
    help='Config path',
    show_default=True
)
@click.option(
    '-l', '--login',
    is_flag=True
)
@pass_context
def queue(ctx, config, login):
    username = getpass.getuser()
    if login:
        password = prompt(text='Password', hide_input=True)
    else:
        password = None
    try:
        ctx.obj = make_app(
            config_path=config,
            username=username,
            password=password,
        )
    except NoCookieException:
        password = prompt(text='Password', hide_input=True)
        ctx.obj = make_app(
            config_path=config,
            username=username,
            password=password,
        )


@click.argument('command')
@queue.command()
@pass_context
def work(ctx, command):
    app = ctx.obj
    app.request(
        method='POST',
        path='/users/{username}/works'.format(username=app.username),
        json={
            'command': command,
            'cwd': os.getcwd()
        }
    )


@click.argument('work_id')
@queue.command()
@pass_context
def kill(ctx, work_id):
    app = ctx.obj
    app.request(
        method='DELETE',
        path='/users/{username}/works/{work_id}'.format(
            username=app.username,
            work_id=work_id
        ),
    )


@queue.command()
@pass_context
def list(ctx):
    app = ctx.obj
    app.request(
        method='GET',
        path='/users/{username}/works'.format(
            username=app.username
        )
    )


@click.argument('work_id')
@queue.command()
@pass_context
def details(ctx, work_id):
    app = ctx.obj
    app.request(
        method='GET',
        path='/users/{username}/works/{work_id}'.format(
            username=app.username,
            work_id=work_id
        )
    )
