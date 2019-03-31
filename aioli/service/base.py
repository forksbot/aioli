# -*- coding: utf-8 -*-

from uvloop.loop import Loop

from aioli import Application
from aioli.core.component import BaseComponent


class BaseService(BaseComponent):
    """The Service base class used for creating Package Services, it implements the
    singleton pattern as Services are commonly used in many parts of a Package.

    :ivar app: Aioli application instance
    :ivar loop: Asyncio event loop (uvloop)
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(BaseService, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    app: Application
    loop: Loop

    def on_ready(self):
        """Called upon initialization"""

    @classmethod
    def register(cls, pkg, mgr):
        """Class method used internally by the Aioli manager to register a Service

        :param pkg: instance of :class:`aioli.Package`
        :param mgr: instance of :class:`Aioli.AioliManager`
        """

        cls.loop = mgr.loop
        cls.app = mgr.app
        cls._pkg_bind(pkg)
