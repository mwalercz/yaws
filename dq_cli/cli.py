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
def works(ctx):
    pass


@click.option('-d', '--directory', default=os.getcwd())
@click.argument('command')
@works.command()
@pass_context
def submit(ctx, command, directory):
    c = ctx.obj
    c('controller').request(
        method='POST',
        path='/users/{username}/works'.format(username=c('username')),
        json={
            'command': command,
            'cwd': directory,
        }
    )


@click.argument('work_id')
@works.command()
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


@works.command()
@pass_context
@click.option('-s', '--status', multiple=True)
def query(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users/{username}/works'.format(
            username=c('username')
        )
    )


@click.argument('work_id')
@works.command()
@pass_context
def info(ctx, work_id):
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
def info(ctx, worker_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/workers/{}'.format(worker_id)
    )
