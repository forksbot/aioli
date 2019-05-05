# -*- coding: utf-8 -*-

import asyncio
import logging
import inspect

import sqlalchemy
from starlette.applications import Starlette
from aiohttp import ClientSession

from aioli.exceptions import InternalError
from aioli.core.package import Package
from aioli.db import DatabaseManager


class Manager:
    """Takes care of package registration and injection upon application start"""

    pkgs = []
    app: Starlette = None
    db = DatabaseManager
    loop = asyncio.get_event_loop()
    http_client: ClientSession
    log = logging.getLogger('aioli.manager')

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
            if not hasattr(module, 'export'):
                raise Exception(f'Missing package export in {module}')
            elif not isinstance(module.export, Package):
                raise Exception(f'Invalid package type {module.export}: must be of type {Package}')

            export = module.export

            if export.name in dict(self.pkgs).keys():
                raise Exception(f'Duplicate package name {export.name}')

            export.version = getattr(module, '__version__', '0.0.0')
            export.path = assigned_path

            self.log.info(f'Attaching {export.name}/{export.version}')

            self.pkgs.append((export.name, export))

    async def _register_services(self):
        """Registers Services with Application"""

        for pkg_name, pkg in self.pkgs:
            for svc in pkg.services:
                svc.register(pkg, self)
                svc_obj = svc()

                if inspect.iscoroutinefunction(svc_obj.on_ready):
                    await svc_obj.on_ready()
                else:
                    svc_obj.on_ready()

                pkg.log.info(f'Service {svc.__name__} initialized')

    async def _register_models(self):
        """Registers Models with the application and performs table creation"""

        models = list(self.models)

        if models and not self.db.database:
            raise InternalError('Unable to register models without a database connection')

        engine = sqlalchemy.create_engine(self.db.url)

        for pkg, model in models:
            model.__database__ = self.db.database
            pkg.log.debug(f'Registering model: {model.__name__} [{model.__table__.name}]')

        self.db.metadata.create_all(engine)

    async def _register_controllers(self):
        """Registers Controllers with Application"""

        for pkg_name, pkg in self.pkgs:
            pkg.log.info('Controller initializing')
            path_base = self.app.config['API_BASE']

            # Make package available to Controller
            pkg.controller.register(pkg)
            ctrl = pkg.controller = pkg.controller()

            # Iterate over route stacks and register routes with the application
            for handler, route in ctrl.stacks:
                handler_addr = hex(id(handler))
                handler_name = f'{pkg_name}.{route.name}'
                import re

                def format_path(*parts):
                    path = ''

                    for part in parts:
                        path = f'/{path}/{part}'

                    return re.sub(r'/+', '/', path.rstrip('/'))

                path_full = format_path(path_base, pkg.path, route.path)
                print(path_full)
                pkg.log.debug(
                    f'Registering route: {path_full} [{route.method}] => '
                    f'{route.name} [{handler_addr}]'
                )

                methods = [route.method]
                self.app.add_route(path_full, handler, methods, handler_name)

                # Inject full path into handler
                route.path_full = path_full

            # Let the Controller know we're ready to receive requests
            if inspect.iscoroutinefunction(ctrl.on_ready):
                await ctrl.on_ready()
            else:
                ctrl.on_ready()

            pkg.log.info('Controller initialized')

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
        if app.config['DB_URL']:
            self.db = await DatabaseManager.init(app.config['DB_URL'])
            await self._register_models()

        await self._register_controllers()
        await self._register_services()

        # app.log.info(f'Worker {getpid()} ready for action')
        self.log.info('Components loaded')


mgr = Manager()
