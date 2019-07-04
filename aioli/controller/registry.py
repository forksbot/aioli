class RequestSchema:
    _parts = {}

    @property
    def parts(self):
        return self._parts

    def __iter__(self):
        return self._parts

    def __setattr__(self, key, value):
        self._parts[key] = value

    def __getattr__(self, key):
        if key in self._parts:
            return self._parts[key]

    def from_dict(self, **schemas):
        for key, schema in schemas.items():
            self._parts[key] = schema


class RouteStack:
    """Keeps track of decorators applied to a route handler"""

    handler = None
    name = None
    path = None
    method = None
    description = None

    def __init__(self):
        self.schemas = RequestSchema()

    def __dict__(self):
        return self.__class__.__dict__

    def add_route(self, handler, path, method, description):
        """Adds new route to the stack

        :param handler: Route handler function
        :param path: Route path
        :param method: Route method
        :param description: Endpoint description
        """

        self.handler = handler
        self.name = handler.__name__
        self.path = path
        self.method = method
        self.description = description


class RouteRegistry:
    """Keeps track of all RouteStacks in the application"""

    stacks = {}

    @classmethod
    def get_stack(cls, handler):
        """Get (or create) new RouteStack for a handler

        :param handler: route handler
        :return: RouteStack instance
        """

        hid = hash(handler.__module__ + handler.__name__)

        if hid not in cls.stacks:
            cls.stacks[hid] = RouteStack()

        return cls.stacks[hid]
