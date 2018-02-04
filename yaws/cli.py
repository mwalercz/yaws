import getpass
import os

import click
from click import pass_context

from yaws.app import make_app
from yaws.exceptions import NoCookieException


@click.group()
@click.option('-u', '--username', default=None)
@click.option('-p', '--password', is_flag=True, default=None)
@pass_context
def yaws(ctx, username, password):
    if password:
        password = getpass.unix_getpass()
    try:
        ctx.obj = make_app(
            cli_username=username,
            cli_password=password,
        )
    except NoCookieException:
        password = getpass.unix_getpass()
        ctx.obj = make_app(
            cli_username=username,
            cli_password=password,
        )


@click.option('-d', '--directory', default=os.getcwd())
@click.argument('command')
@yaws.command()
@pass_context
def submit(ctx, command, directory):
    c = ctx.obj
    c('controller').request(
        method='POST',
        path='/works',
        json={
            'command': command,
            'cwd': directory,
        }
    )


@click.argument('work_id')
@yaws.command()
@pass_context
def cancel(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='DELETE',
        path='/works/{work_id}'.format(
            work_id=work_id
        ),
    )


@yaws.command()
@pass_context
@click.option('-s', '--status', multiple=True)
def query(ctx, status):
    c = ctx.obj
    statuses = [
        ('status', s) for s in status
    ]
    c('controller').request(
        method='GET',
        path='/works',
        params=statuses
    )


@click.argument('work_id')
@yaws.command()
@pass_context
def info(ctx, work_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/works/{work_id}'.format(
            work_id=work_id
        )
    )


@yaws.group()
@pass_context
def workers(ctx):
    pass


@workers.command(name='query')
@pass_context
def workers_query(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/workers'
    )


@click.argument('worker_id')
@workers.command(name='info')
@pass_context
def worker_info(ctx, worker_id):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/workers/{}'.format(worker_id)
    )


@yaws.group()
@pass_context
def users(ctx):
    pass


@click.argument('username')
@click.option('-a', '--is_admin', is_flag=True, default=False)
@users.command(name='register')
@pass_context
def register_user(ctx, username, is_admin):
    c = ctx.obj
    c('controller').request(
        method='POST',
        path='/users',
        json={
            'username': username,
            'is_admin': is_admin,
        }
    )


@users.command(name='query')
@pass_context
def users_query(ctx):
    c = ctx.obj
    c('controller').request(
        method='GET',
        path='/users',
    )
