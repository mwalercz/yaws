import getpass
import os

import click
from click import pass_context
from click import prompt

from dq_cli.app import init_app
from dq_cli.exceptions import NoCookieException


@click.group()
@click.option(
    '-u', '--username',
)
@click.option(
    '-p', '--password',
    is_flag=True
)
@pass_context
def queue(ctx, password, username):
    if not username:
        username = getpass.getuser()
    if password:
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


@queue.group()
@pass_context
def work(ctx):
    pass


@click.option('--cwd', default=os.getcwd())
@click.option('-c', '--command', required=True)
@work.command()
@pass_context
def new(ctx, command, cwd):
    c = ctx.obj
    c('controller').request(
        method='POST',
        path='/users/{username}/works'.format(username=c('username')),
        json={
            'command': command,
            'cwd': cwd,
        }
    )


@click.argument('work_id')
@work.command()
@pass_context
def cancel(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='DELETE',
        path='/users/{username}/works/{work_id}'.format(
            username=c('username'),
            work_id=work_id
        ),
    )


@work.command()
@pass_context
def query(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users/{username}/works'.format(
            username=c('username')
        )
    )


@click.argument('work_id')
@work.command()
@pass_context
def get(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users/{username}/works/{work_id}'.format(
            username=c('username'),
            work_id=work_id
        )
    )


@queue.group()
@pass_context
def workers(ctx):
    pass


@workers.command()
@pass_context
def query(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/workers'
    )


@click.argument('worker_id')
@workers.command()
@pass_context
def get(ctx, worker_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/workers/{}'.format(worker_id)
    )
