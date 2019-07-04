from functools import wraps

from starlette.requests import Request
from starlette.responses import Response

from aioli.exceptions import AioliException

from .consts import Method, RequestProp
from .registry import RouteRegistry


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

    header = schemas.get("header")
    body = schemas.get("body")
    path = schemas.get("path")
    query = schemas.get("query")

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

            if header:
                kwargs.update({"header": header().load(request.headers)})

            if path:
                kwargs.update(path().load(request.path_params))

            if body:
                payload = await request.json()
                kwargs.update({"body": body().load(payload)})

            if query:
                kwargs.update({"query": query().load(request.query_params)})

            return await fn(*args_new, **kwargs)

        stack = RouteRegistry.get_stack(handler)

        # Add the provided schemas to the RouteStack
        stack.schemas.from_dict(**schemas)

        return handler

    return wrapper


def returns(schema_cls=None, status=200, many=False):
    """Returns a transformed and serialized Response

    :param schema_cls: Marshmallow.Schema class
    :param status: Return status (on success)
    :param many: Whether to return a list or single object
    :return: Response
    """

    obj = schema_cls(many=many) if schema_cls else None

    def wrapper(fn):
        @wraps(fn)
        async def handler(*args, **kwargs):
            args_new = list(args)

            # Remove `Request` object from args (in case it wasn't consumed by an `input_local`).
            if len(args) > 1 and isinstance(args[1], Request):
                args_new.pop(1)

            rv = await fn(*args_new, **kwargs)
            data = (
                obj.dumps(rv, indent=4, ensure_ascii=False).encode("utf8")
                if obj
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
        stack.schemas.response = schema_cls

        return handler

    return wrapper
