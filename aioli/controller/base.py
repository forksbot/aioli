import re

from starlette.endpoints import WebSocketEndpoint

from aioli.component import Component, ComponentMeta

from .registry import handlers


def format_path(*parts):
    path = ""

    for part in parts:
        path = f"/{path}/{part}"

    return re.sub(r"/+", "/", path.rstrip("/"))


class HttpControllerMeta(ComponentMeta):
    def __call__(cls, pkg, *args, **kwargs):
        ctrl = super(HttpControllerMeta, cls).__call__(pkg, *args, **kwargs)
        app = pkg.app

        for func, handler in ctrl.handlers:
            handler_addr = hex(id(func))
            handler_name = f"{ctrl.__class__.__name__}.{handler.name}"

            path_full = format_path(app.config["api_base"], pkg.path, handler.path)

            if not hasattr(ctrl, "pkg"):
                raise Exception(f"Superclass of {ctrl} was never created")

            ctrl.log.info(
                f"Registering Route: {path_full} [{handler.method}] => "
                f"{handler.name} [{handler_addr}]"
            )

            methods = [handler.method]

            app.add_route(path_full, func, methods, handler_name)
            handler.path_full = path_full

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
    def handlers(self):
        for handler in handlers.values():
            # Yield only if the stack belongs to the Controller being iterated on
            if handler.func.__module__ == self.__module__:
                yield getattr(self, handler.name), handler


class BaseWebSocketController(WebSocketEndpoint, Component, metaclass=ComponentMeta):
    path = None
    encoding = "json"
