# -*- coding: utf-8 -*-

import asyncio
import logging
import inspect

import sqlalchemy
from aiohttp import ClientSession

from aioli.exceptions import InternalError
from aioli.db import DatabaseManager
from aioli.utils.http import format_path
from aioli.package.controller import BaseHttpController, BaseWebSocketController

from .package import Package


class Manager:
    """Takes care of registering packages, implements the Singleton pattern"""

    __instance = None

    pkgs = []
    app = None
    db = DatabaseManager
    loop = asyncio.get_event_loop()
    http_client: ClientSession
    log = logging.getLogger("aioli.manager")

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Manager, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    @property
    def models(self):
        """Yields a list of package-model tuples"""

        for pkg_name, pkg in self.pkgs:
            for model in pkg.models:
                yield pkg, model

    def get_pkg(self, name):
        """Get package by name"""

        return dict(self.pkgs).get(name)

    def _load_packages(self, pkg_modules):
        """Takes a list of Packages, tests their sanity and registers with manager"""

        for assigned_path, module in pkg_modules:
            if not hasattr(module, "export"):
                raise Exception(f"Missing package export in {module}")
            elif not isinstance(module.export, Package):
                raise Exception(
                    f"Invalid package type {module.export}: must be of type {Package}"
                )

            export = module.export

            if export.name and export.name in dict(self.pkgs).keys():
                raise Exception(f"Duplicate package name {export.name}")
            if assigned_path:
                export.path = assigned_path

            export.version = getattr(module, "__version__", "0.0.0")

            self.log.info(f"Attaching {export.name}/{export.version}")
            self.pkgs.append((export.name, export))

    async def _register_services(self):
        """Registers Services with Application"""

        for pkg_name, pkg in self.pkgs:
            for svccls in pkg.services:
                pkg.log.debug(f"Service {svccls.__name__} initializing")

                svccls.register(pkg, self)
                svc = svccls()

                if inspect.iscoroutinefunction(svc.on_ready):
                    await svc.on_ready()
                else:
                    svc.on_ready()

    async def _register_models(self):
        """Registers Models with the application and performs table creation"""

        models = list(self.models)

        if models and not self.db.database:
            raise InternalError(
                "Unable to register models without a database connection"
            )

        engine = sqlalchemy.create_engine(self.db.url)

        for pkg, model in models:
            model.__database__ = self.db.database
            pkg.log.debug(
                f"Registering model: {model.__name__} [{model.__table__.name}]"
            )

        self.db.metadata.create_all(engine)

    async def _register_http_controller(self, pkg, ctrlcls):
        ctrlcls.register(pkg)
        ctrl = ctrlcls()

        # Iterate over route stacks and register routes with the application
        for handler, route in ctrl.stacks:
            handler_addr = hex(id(handler))
            handler_name = f"{pkg.name}.{route.name}"

            path_full = format_path(self.app.config["API_BASE"], pkg.path, route.path)
            pkg.log.debug(
                f"Registering route: {path_full} [{route.method}] => "
                f"{route.name} [{handler_addr}]"
            )

            methods = [route.method]

            self.app.add_route(path_full, handler, methods, handler_name)

            # Inject full path into handler
            route.path_full = path_full

        await ctrl.on_ready()

    async def _register_ws_controller(self, pkg, ctrlcls):
        assert ctrlcls.path, "Missing WebSocket path"

        ctrlcls.register(pkg)

        path_full = format_path(self.app.config["API_BASE"], pkg.path, ctrlcls.path)

        pkg.log.debug(f"Registering WebSocket route: {path_full}")

        self.app.add_websocket_route(path_full, ctrlcls, "test")

    async def _register_controller(self, pkg, ctrlcls):
        if issubclass(ctrlcls, BaseWebSocketController):
            return await self._register_ws_controller(pkg, ctrlcls)

        return await self._register_http_controller(pkg, ctrlcls)

    async def _register_controllers(self):
        """Registers Controllers with Application"""

        for pkg_name, pkg in self.pkgs:
            if not pkg.path:
                continue

            pkg.log.debug(f"Registering controllers")

            for ctrlcls in pkg.controllers:
                assert issubclass(ctrlcls, BaseHttpController) or issubclass(
                    ctrlcls, BaseWebSocketController
                )

                pkg.log.debug(f"Controller {ctrlcls.__name__} initializing")

                await self._register_controller(pkg, ctrlcls)

    async def detach(self, *_):
        """Application stop-handler"""

        await self.http_client.close()

    async def attach(self, app):
        """Application start-handler

        Sets up DB and HTTP clients, followed by component registration.

        :param app: Instance of aioli.Application
        """

        self._load_packages(app.packages)
        self.app = app

        # self.loop = loop

        # self.http_client = ClientSession(loop=loop)
        if app.config["DB_URL"]:
            self.db = await DatabaseManager.init(app.config["DB_URL"])
            await self._register_models()

        await self._register_controllers()
        await self._register_services()

        # app.log.info(f'Worker {getpid()} ready for action')
        self.log.info("Components loaded")
