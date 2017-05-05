import os
from omi_api.server import create_server


def main():
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
        'threads': 1,
        # TODO: Remove this again
        'debug': True,
    }
    app_server = create_server(settings)
    app_server.run()


if __name__ == '__main__':
    main()
