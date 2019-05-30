# -*- coding: utf-8 -*-

from starlette.endpoints import WebSocketEndpoint

from aioli.registry import RouteRegistry

from .._component import Component


class ControllerComponent(Component):
    @classmethod
    def register(cls, pkg):
        """Makes the package available to this controller.

        :param pkg: aioli.Package
        """

        cls._pkg_bind(pkg)


class BaseHttpController(ControllerComponent):
    async def on_request(self, *args):
        """Called upon request arrival"""

    @property
    def stacks(self):
        """Route stack iterator

        Iterates over RouteStacks, takes the stack.name (which corresponds to the handler function name)
        and returns reference to its instance method, along with the stack itself (schemas, paths, methods etc).

        :return: (<handler name>, <stack>)
        """

        for stack in RouteRegistry.stacks.values():
            # Yield only if the stack belongs to the Controller being iterated on
            if stack.handler.__module__ == self.__module__:
                yield getattr(self, stack.name), stack


class BaseWebSocketController(ControllerComponent, WebSocketEndpoint):
    path = None
    encoding = "json"
