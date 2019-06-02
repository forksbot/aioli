# -*- coding: utf-8 -*-

import re

NAME_REGEX = re.compile(r"^[a-zA-Z0-9-]*$")
PATH_REGEX = re.compile(r"^/[a-zA-Z0-9-]*$")

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

    :param name: Package name
    :param description: Package description
    :param version: Package semver version
    :param controllers: List of Controller classes
    :param services: List of Service classes
    :param models: List of Model classes
    """

    _name = None
    _version = None

    def __init__(
        self,
        name,
        description,
        version,
        controllers=None,
        services=None,
        models=None,
    ):
        assert isinstance(controllers, list) or None
        assert isinstance(services, list) or None

        self.name = name
        self.description = description
        self.version = version

        self.controllers = controllers or []
        self.services = services or []
        self.models = models or []

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if not VERSION_REGEX.match(value):
            raise Exception(
                f"Package {self.name} version is not a valid semver version string"
            )

        self._version = value

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
