"""This module contains basic functions to instantiate the BigchainDB API.

The application is implemented in Flask and runs using Gunicorn.
"""

import copy
import multiprocessing

import gunicorn.app.base

from flask import Flask
from flask_cors import CORS

from omi_api.views.recordings import recording_views
from omi_api.views.compositions import composition_views
from omi_api.views.recordings_compositions import recordings_compositions_views


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    """Run a **wsgi** app wrapping it in a Gunicorn Base Application.

    Adapted from:
     - http://docs.gunicorn.org/en/latest/custom.html
    """

    def __init__(self, app, options=None):
        '''Initialize a new standalone application.

        Args:
            app: A wsgi Python application.
            options (dict): the configuration.

        '''
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict((key, value) for key, value in self.options.items()
                      if key in self.cfg.settings and value is not None)

        for key, value in config.items():
            # not sure if we need the `key.lower` here, will just keep
            # keep it for now.
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def create_app(settings):
    """Return an instance of the Flask application.

    Args:
        debug (bool): a flag to activate the debug mode for the app
            (default: False).
    """

    app = Flask(__name__)

    if not settings.get('cors_protection', True):
        CORS(app)

    app.debug = settings.get('debug', False)

    app.register_blueprint(composition_views, url_prefix='/api/v1')
    app.register_blueprint(recording_views, url_prefix='/api/v1')
    app.register_blueprint(recordings_compositions_views, url_prefix='/api/v1')
    return app


def create_server(settings):
    """Wrap and return an application ready to be run.

    Args:
        settings (dict): a dictionary containing the settings, more info
            here http://docs.gunicorn.org/en/latest/settings.html

    Return:
        an initialized instance of the application.
    """

    settings = copy.deepcopy(settings)

    if not settings.get('workers'):
        settings['workers'] = (multiprocessing.cpu_count() * 2) + 1

    if not settings.get('threads'):
        settings['threads'] = (multiprocessing.cpu_count() * 2) + 1

    app = create_app(settings)
    standalone = StandaloneApplication(app, settings)
    return standalone
