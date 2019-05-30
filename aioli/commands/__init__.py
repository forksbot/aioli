# -*- coding: utf-8 -*-

import click
from uvicorn import run as run_server


@click.group()
def cli():
    pass


@click.command()
@click.option('--host', default='127.0.0.1', help='Bind socket to this host.')
@click.option('--port', default=5000, help='Bind socket to this port.')
@click.argument('app')
def start_dev(host, port, app):
    run_server(app, host=host, port=port, reload=True, debug=True, workers=1, log_level='debug', loop='uvloop')


cli.add_command(start_dev)
