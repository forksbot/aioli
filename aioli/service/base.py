# -*- coding: utf-8 -*-

from uvloop.loop import Loop

from aioli import Application
from aioli.core.component import BaseComponent
from .db import DatabaseService, DatabaseManager


class BaseService(BaseComponent):
    """The Service base class used for creating Package Services, it implements the
    singleton pattern as Services are commonly used in many parts of a Package.

    :ivar app: Aioli application instance
    :ivar loop: Asyncio event loop (uvloop)
    """

    __model__ = None
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(BaseService, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    app: Application
    loop: Loop
    _db = None
    db_manager: DatabaseManager

    def on_ready(self):
        if self.__model__:
            self._db = DatabaseService(self.db_manager, self.__model__)

    @property
    def db(self) -> DatabaseService:
        return self._db

    @classmethod
    def register(cls, pkg, manager):
        """Class method used internally by the Aioli manager to register a Service

        :param pkg: instance of :class:`aioli.Package`
        :param manager: instance of :class:`Aioli.Manager`
        """

        cls.loop = manager.loop
        cls.app = manager.app
        cls.pkgs = manager.pkgs
        cls.db_manager = manager.db
        cls._pkg_bind(pkg)
