import getpass
import os

import click
from click import pass_context
from click import prompt

from dq_cli.app import init_app
from dq_cli.exceptions import NoCookieException


@click.group()
@click.option(
    '-l', '--login',
    is_flag=True
)
@pass_context
def queue(ctx, login):
    username = getpass.getuser()
    if login:
        password = prompt(text='Password', hide_input=True)
    else:
        password = None
    try:
        ctx.obj = init_app(
            username=username,
            password=password,
        )
    except NoCookieException:
        password = prompt(text='Password', hide_input=True)
        ctx.obj = init_app(
            username=username,
            password=password,
        )


@click.argument('command')
@queue.command()
@pass_context
def work(ctx, command):
    c = ctx.obj
    c('controller').request(
        method='POST',
        path='/users/{username}/works'.format(username=c('username')),
        json={
            'command': command,
            'cwd': os.getcwd()
        }
    )


@click.argument('work_id')
@queue.command()
@pass_context
def kill(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='DELETE',
        path='/users/{username}/works/{work_id}'.format(
            username=c('username'),
            work_id=work_id
        ),
    )


@queue.command()
@pass_context
def list(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users/{username}/works'.format(
            username=c('username')
        )
    )


@click.argument('work_id')
@queue.command()
@pass_context
def details(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users/{username}/works/{work_id}'.format(
            username=c('username'),
            work_id=work_id
        )
    )
