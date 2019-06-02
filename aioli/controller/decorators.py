# -*- coding: utf-8 -*-

"""
Route decorators are executed in the reversed order.
output_dump -> input_load -> route
"""

from functools import wraps

from starlette.requests import Request
from starlette.responses import Response

from aioli.registry import RouteRegistry
from aioli.exceptions import AioliException

from .consts import Method, RequestProp


def route(path, method, description=None):
    """Prepares route registration, and performs handler injection.

    :param path: Handler path, relative to application and package paths
    :param method: HTTP Method
    :param description: Endpoint description
    :return: Route handler
    """

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            return await fn(*args, **kwargs)

        if not isinstance(method, Method):
            raise AioliException(
                f"Invalid HTTP method supplied in @route for handler: {handler}. "
                f"Must be of type: {Method.__module__}.{Method.__name__}"
            )

        stack = RouteRegistry.get_stack(handler)

        # Adds the handler for registration once the loop is ready.
        stack.add_route(handler, path, method.value, description)

        return handler

    return wrapper


def takes(props=None, **schemas):
    """Takes a list of schemas used to validate and transform parts of a request object.
    The selected parts are injected into the route handler as arguments.

    :param props: List of `Pluck` targets
    :param schemas: list of schemas (kwargs)
    :return: Route handler
    """

    props = props or []
    schemas = {part: schema() for part, schema in schemas.items()}

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            args_new = list(args)
            request = kwargs["request"] if "request" in kwargs else args_new.pop(1)

            for prop in props:
                value = RequestProp(prop).value
                assert "." in value

                target = request

                for member in value.split("."):
                    target = getattr(target, member)

                kwargs.update({RequestProp(prop).name: target})

            if "headers" in schemas:
                kwargs.update({"headers": schemas["headers"].load(request.headers)})

            if "path" in schemas:
                kwargs.update(schemas["path"].load(request.path_params))

            if "body" in schemas:
                payload = await request.json()
                kwargs.update({"body": schemas["body"].load(payload)})

            if "query" in schemas:
                kwargs.update({"query": schemas["query"].load(request.query_params)})

            return await fn(*args_new, **kwargs)

        stack = RouteRegistry.get_stack(handler)

        # Add the provided schemas to the RouteStack
        stack.schemas.update(schemas)

        return handler

    return wrapper


def returns(schema_cls=None, status=200, many=False):
    """Returns a transformed and serialized Response

    :param schema_cls: Marshmallow.Schema class
    :param status: Return status (on success)
    :param many: Whether to return a list or single object
    :return: Response
    """

    schema = schema_cls(many=many) if schema_cls else None

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            args_new = list(args)

            # Remove `Request` object from args (in case it wasn't consumed by an `input_local`).
            if len(args) > 1 and isinstance(args[1], Request):
                args_new.pop(1)

            rv = await fn(*args_new, **kwargs)
            data = (
                schema.dumps(rv, indent=4, ensure_ascii=False).encode("utf8")
                if schema
                else None
            )

            # Return HTTP encoded JSON response
            return Response(
                content=data,
                status_code=status,
                headers={"content-type": "application/json"},
            )

        stack = RouteRegistry.get_stack(handler)

        # Add the `response` schema to this route handler's stack
        stack.schemas.update({"response": schema})

        return handler

    return wrapper
