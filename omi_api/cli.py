import os

import click
from bigchaindb_driver.crypto import generate_keypair

from omi_api.server import create_server


@click.group()
def cli():
    pass


@cli.command()
def keypair():
    keypair = generate_keypair()
    click.echo(click.style('Copy paste those values in your env file:', fg='white'))
    click.echo(click.style('OMI_PUBLIC_KEY={}'.format(keypair.public_key), fg='green'))
    click.echo(click.style('OMI_PRIVATE_KEY={}'.format(keypair.private_key), fg='green'))



@cli.command()
def run():
    # Double check in case the environment variable is sent via Docker,
    # which will send empty strings for missing environment variables
    hostname = os.environ.get('API_HOST', None)
    if not hostname:
        hostname = 'localhost'

    port = os.environ.get('API_PORT', None)
    if not port:
        port = '3000'

    cors_protection = os.environ.get('CORS_PROTECTION', 'True') == 'True'

    # start the web api
    settings = {
        'bind': '{hostname}:{port}'.format(hostname=hostname, port=port),
        'cors_protection': cors_protection,
        'workers': 1,
        'threads': 1
    }
    app_server = create_server(settings)
    app_server.run()


if __name__ == '__main__':
    run()
