# -*- coding: utf-8 -*-

import re
from logging import getLogger

NAME_REGEX = re.compile(r'^[a-zA-Z0-9-]*$')
PATH_REGEX = re.compile(r'^/[a-zA-Z0-9-]*$')


class Package:
    """Associates components and meta with a package, for registration with a Aioli Application.

    :param name: Package name
    :param description: Package description
    :param controllers: List of Controller classes
    :param services: List of Service classes
    :param models: List of Model classes
    """

    _path = None
    _name = None

    def __init__(self, name, description, controllers=None, services=None, models=None, dependencies=None):
        assert isinstance(controllers, list) or None
        assert isinstance(services, list) or None

        self.name = name

        self.controllers = controllers or []
        self.services = services or []
        self.models = models or []
        self.dependencies = dependencies or []

        self.log = getLogger(f'aioli.pkg.{self.name}')
        self.description = description

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not NAME_REGEX.match(value):
            raise Exception(
                f'Invalid identifier "{value}" - may only contain alphanumeric and hyphen characters.'
            )

        self._name = value

    @property
    def path(self):
        """Package path accessor"""

        return self._path

    @path.setter
    def path(self, value):
        if not PATH_REGEX.match(value):
            raise Exception(f'Package {self.name} path must be a valid path, example: /my-package-1')

        self._path = value

    def __repr__(self):
        return f'<{self.__class__.__name__} [{self.name}] at {hex(id(self))}>'
