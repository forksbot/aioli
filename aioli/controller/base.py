import re

from starlette.endpoints import WebSocketEndpoint

from aioli.component import Component, ComponentMeta

from .registry import RouteRegistry


def format_path(*parts):
    path = ""

    for part in parts:
        path = f"/{path}/{part}"

    return re.sub(r"/+", "/", path.rstrip("/"))


class HttpControllerMeta(ComponentMeta):
    def __call__(cls, pkg, *args, **kwargs):
        ctrl = super(HttpControllerMeta, cls).__call__(pkg, *args, **kwargs)
        app = pkg.app

        for handler, route in ctrl.stacks:
            handler_addr = hex(id(handler))
            handler_name = f"{ctrl.__class__.__name__}.{route.name}"

            path_full = format_path(app.config["api_base"], pkg.path, route.path)

            if not hasattr(ctrl, "pkg"):
                raise Exception(f"Superclass of {ctrl} was never created")

            ctrl.log.info(
                f"Registering Route: {path_full} [{route.method}] => "
                f"{route.name} [{handler_addr}]"
            )

            methods = [route.method]

            app.add_route(path_full, handler, methods, handler_name)
            route.path_full = path_full

        return ctrl


class BaseHttpController(Component, metaclass=HttpControllerMeta):
    """HTTP API Controller

    :param pkg: Attach to this package

    :var pkg: Parent Package
    :var config: Package configuration
    :var log: Controller logger
    """

    async def on_request(self, *args):
        """Called on request arrival for this Controller"""

    @property
    def stacks(self):
        for stack in RouteRegistry.stacks.values():
            # Yield only if the stack belongs to the Controller being iterated on
            if stack.handler.__module__ == self.__module__:
                yield getattr(self, stack.name), stack


class BaseWebSocketController(WebSocketEndpoint, Component, metaclass=ComponentMeta):
    path = None
    encoding = "json"
