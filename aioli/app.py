# -*- coding: utf-8 -*-

import logging
import logging.config
import traceback

from json.decoder import JSONDecodeError
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from marshmallow.exceptions import ValidationError

from aioli.exceptions import HTTPException, AioliException
from aioli.log import LOGGING_CONFIG_DEFAULTS
from aioli.utils.http import jsonify
from .config import ConfigConsumer
from .manager import PackageManager


async def server_error(_, exc):
    if isinstance(exc, NotImplementedError):
        message = "Not implemented"
    else:
        message = "Internal server error"

    return jsonify({"message": message}, status=500)


async def validation_error(_, exc):
    return jsonify({"message": exc.messages}, status=422)


async def decode_error(*_):
    return jsonify({"message": "Error decoding JSON"}, status=400)


async def http_error(_, exc):
    return jsonify({"message": exc.detail}, status=exc.status_code)


class Application(Starlette):
    """Creates an Aioli application

    :param packages: List of package tuples [("<path>", <pkg>), ...]
    :param listen_host: Bind socket to this host
    :param listen_port: Bind socket to this port
    :param debug: Debug mode
    :param workers: Worker count
    :param api_base: API base path
    :param db_url: SQLAlchemy database URL
    :param kwargs: Kwargs to pass along to Starlette
    """

    log = logging.getLogger("aioli")

    async def startup(self):
        try:
            await self.pkg_mgr.attach(self)
            self.log.info("Ready for action")
        except Exception as e:
            self.log.critical(traceback.format_exc())
            raise e

    async def shutdown(self):
        self.pkg_mgr.log.info("Disconnecting from database...")
        await self.pkg_mgr.db.database.disconnect()

    def __init__(self, packages, **kwargs):
        if not packages:
            raise Exception(
                f"aioli.Application expects an iterable of packages, got: {type(packages)}"
            )

        self.packages = packages

        try:
            overrides = dict(kwargs or {})
        except ValueError:
            raise Exception("Application `settings` must be a collection")

        self.pkg_mgr = PackageManager()

        for name, logger in LOGGING_CONFIG_DEFAULTS['loggers'].items():
            self.log_level = logger['level'] = 'DEBUG' if overrides.get('debug') else 'INFO'

        logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)

        self.log.info("Commencing countdown, engines on")

        # Apply known settings from ENV or provided `settings`
        cc = ConfigConsumer(overrides)
        self.config = cc.consumed

        # Pass the remainder arguments to Starlette
        super(Application, self).__init__(**cc.consumables)

        # Lifespan handlers
        self.router.lifespan.add_event_handler("startup", self.startup)
        self.router.lifespan.add_event_handler("shutdown", self.shutdown)

        # Error handlers
        self.add_exception_handler(AioliException, http_error)
        self.add_exception_handler(HTTPException, http_error)
        self.add_exception_handler(ValidationError, validation_error)
        self.add_exception_handler(JSONDecodeError, decode_error)
        self.add_exception_handler(Exception, server_error)

        # Middleware
        self.add_middleware(CORSMiddleware, allow_origins=["*"])
