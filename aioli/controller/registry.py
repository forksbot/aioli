handlers = {}


class HandlerMeta(type):
    def __call__(cls, func):
        fid = hash(func.__module__ + func.__name__)

        if fid not in handlers:
            handlers[fid] = super(HandlerMeta, cls).__call__(func)

        return handlers[fid]


class HandlerSchema:
    def __init__(self):
        self.body = None
        self.path = None
        self.header = None
        self.query = None
        self.response = None

    def __iter__(self):
        for location, schema in self.__dict__.items():
            yield location, schema

    def from_dict(self, **schemas):
        for key, schema in schemas.items():
            setattr(self, key, schema)


class Handler(metaclass=HandlerMeta):
    """Keeps track of decorators applied to a route handler"""

    name = None
    path = None
    path_full = None
    status = None
    method = None
    description = None
    _schemas = None

    @property
    def schemas(self):
        if not self._schemas:
            self._schemas = HandlerSchema()

        return self._schemas

    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __dict__(self):
        return self.__class__.__dict__

    def register_route(self, path, method, description):
        """Adds new route to the stack

        :param path: Route path
        :param method: Route method
        :param description: Endpoint description
        """

        self.path = path
        self.method = method
        self.description = description
