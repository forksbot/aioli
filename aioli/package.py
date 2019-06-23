# -*- coding: utf-8 -*-

import logging
import re

from marshmallow.exceptions import ValidationError
from aioli.config import PackageConfigSchema


NAME_REGEX = re.compile(r"^[a-zA-Z0-9_]*$")
PATH_REGEX = re.compile(r"^/[a-zA-Z0-9-_]*$")

# Semantic version regex
# 1 - Major
# 2 - Minor
# 3 - Patch
# 4 (optional) - Pre-release version info
# 5 (optional) - Metadata (build time, number, etc.)

VERSION_REGEX = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-[a-zA-Z\d][-a-zA-Z.\d]*)?(\+[a-zA-Z\d][-a-zA-Z.\d]*)?$"
)


class Package:
    """Associates components and meta with a package, for registration with a Aioli Application.

    :param name: Package name ([a-z, A-Z, 0-9, -])
    :param description: Package description
    :param version: Package semver version
    :param controllers: List of Controller classes to register with the Package
    :param services: List of Services classes to register with the Package
    :param config: Package Configuration Schema

    :ivar app: Application instance
    :ivar log: Package logger
    :ivar state: Package state
    :ivar config: Package config
    :ivar controllers: List of Controllers registered with the Package
    :ivar services: List of Services registered with the Package
    """

    class State:
        __state = {}

        def __setitem__(self, key, value):
            self.__state[key] = value

        def __getitem__(self, item):
            return self.__state.get(item)

    __name = None
    __version = None
    __path = None

    app = None
    conf = {}
    log: logging.Logger

    services = []
    controllers = []

    def __init__(
        self,
        name,
        description,
        version,
        controllers=None,
        services=None,
        config=None,
    ):
        assert not controllers or isinstance(controllers, list), f"{name} controllers must be a list or None"
        assert not services or isinstance(services, list), f"{name} services must be a list "
        assert name not in ["aioli", "aioli_core"], f"Name {name} is reserved and cannot be used"

        if config is None:
            self.conf_schema = PackageConfigSchema
        elif not issubclass(config, PackageConfigSchema):
            raise Exception(
                f"Invalid config type in {name}: {config}. Must be subclass of {PackageConfigSchema}, or None"
            )
        else:
            self.conf_schema = config

        self.state = Package.State()

        self.name = name
        self.description = description
        self.version = version

        self._services = set(services or [])
        self._controllers = set(controllers or [])

    async def detach_services(self):
        for obj in self.services:
            await obj.on_shutdown()

    async def attach_services(self):
        for obj in self.services:
            await obj.on_startup()

    async def attach_controllers(self):
        for obj in self.services:
            await obj.on_startup()

    async def register(self, app, config):
        self.app = app
        self.log = logging.getLogger(f"aioli.pkg.{self.name}")
        self.path = config.get("path", f"/{self.name}")

        try:
            self.conf = self.conf_schema(self.name).load(config)
        except ValidationError as e:
            raise Exception(f"Package {self.name} failed configuration validation: {e.messages}")

        if self._controllers:
            self.controllers = [ctrl_cls(self) for ctrl_cls in self._controllers]

        self.services = [svc_cls(self) for svc_cls in self._services]

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, value):
        if not self._controllers:
            return

        if not PATH_REGEX.match(value):
            raise Exception(f"Invalid Path provided to Package {self.name}")

        self.__path = value

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        if not VERSION_REGEX.match(value):
            raise Exception(f"Package {self.name} version is not a valid SemVer string")

        self.__version = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not NAME_REGEX.match(value):
            raise Exception(f"Invalid identifier '{value}' - may only contain alphanumeric and underscore characters.")

        self.__name = value
