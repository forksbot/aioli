# -*- coding: utf-8 -*-

import logging
import logging.config
import traceback

from json.decoder import JSONDecodeError
from starlette.applications import Starlette
from marshmallow.exceptions import ValidationError

from aioli.exceptions import HTTPException
from aioli.log import LOGGING_CONFIG_DEFAULTS
from aioli.utils import jsonify
from .settings import ApplicationSettings
from .manager import mgr


async def validation_error(_, exc):
    return jsonify({'message': exc.messages}, status=422)


async def decode_error(*_):
    return jsonify({'message': 'Error decoding JSON'}, status=400)


async def http_error(_, exc):
    return jsonify({'message': exc.detail}, status=exc.status_code)


class Application(Starlette):
    """Creates a Aioli application

    :param packages: List of (<path>, <package>)
    :param path: Application root path
    :param settings: Settings overrides
    :param kwargs: kwargs to pass along to Sanic
    """

    async def startup(self):
        try:
            await mgr.attach(self)
            self.log.info('Ready for action')
        except Exception as e:
            self.log.critical(traceback.format_exc())
            raise e

    async def shutdown(self):
        self.log.info('Disconnecting from database...')
        await mgr.db.database.disconnect()

    def __init__(self, packages=None, path='/api', cors_options=None, settings=None, **kwargs):
        # super(Application, self).__init__(False, [])

        if not packages:
            raise Exception(f'aioli.Application expects an iterable of packages, got: {type(packages)}')

        self.cors_options = cors_options or {}
        self.packages = packages

        try:
            overrides = dict(settings or {})
        except ValueError:
            raise Exception('Application `settings` must be a collection')

        super(Application, self).__init__(
            # log_config=kwargs.pop('log_config', LOGGING_CONFIG_DEFAULTS),
            **kwargs
        )

        for name, logger in LOGGING_CONFIG_DEFAULTS['loggers'].items():
            logger['level'] = 'DEBUG' if overrides.get('DEBUG') else 'INFO'

        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)

        # Application root logger
        self.log = logging.getLogger('aioli.core')
        self.log.info('Commencing countdown, engines on')

        # Apply known settings from ENV or provided `settings`
        self.config = ApplicationSettings(overrides, path).merged

        # Lifespan handlers
        self.router.lifespan.add_event_handler('startup', self.startup)
        self.router.lifespan.add_event_handler('shutdown', self.shutdown)

        # Error handlers
        self.add_exception_handler(HTTPException, http_error)
        self.add_exception_handler(ValidationError, validation_error)
        self.add_exception_handler(JSONDecodeError, decode_error)
