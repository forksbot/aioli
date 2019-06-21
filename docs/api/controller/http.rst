HTTP
====

Creating an HTTP Interface – be it RESTful or otherwise – is done using the
:class:`~aioli.controller.BaseHttpController` class.


*API*

.. automodule:: aioli.controller
.. autoclass:: BaseHttpController
   :members: on_startup, on_shutdown, on_request


*Example – Controller without route handlers*

.. code-block:: python

    from aioli.controller import BaseHttpController

    from .service import VisitService


    class HttpController(BaseHttpController):
        def __init__(self):
            self.visit = VisitService()
            self.log.debug("Guestbook opening")

        async def on_startup(self):
            self.log.debug(f"Guestbook opened at {self.package.path}")

        async def on_request(self, request):
            self.log.debug(f"Request received: {request}")


Routing
-------

Route handlers are standard Python methods decorated with the `@route`.

*API*

.. automodule:: aioli.controller.decorators
   :members: route

*Example – Route handler without transformation helpers*

.. code-block:: python

    from aioli.controller import BaseHttpController, Method, route

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()

        @route("/", Method.GET, "List of entries")
        async def visits_get(self, request):
            # Just pass along the query params as-is.
            #
            # Serialize and return whatever get_many() returns.
            return await self.visit.get_many(**request.query_params)

Transformation
--------------

Transformation is implemented on route handlers using `@takes` and `@returns`. These decorators offer
a simple yet powerful way of shaping and validating request data, while also making sure API endpoints
only returns expected data.

This makes the API more secure and consistent.

Takes
~~~~~

The `@takes` decorator is used to instruct Aioli how to deserialize and validate parts of a request,
and injects the resulting dictionaries as arguments to the decorated function.

*API*

.. automodule:: aioli.controller.decorators
   :noindex:
   :members: takes

*Example – Route handler making use of @takes*

.. code-block:: python

    from aioli.controller import (
        BaseHttpController, ParamsSchema, RequestProp,
        Method, route, takes
    )

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()

        @route("/", Method.GET, "List of entries")
        @takes(query=ParamsSchema)
        async def visits_get(self, query):
            # Transform and validate query params against ParamsSchema,
            # then pass it along to get_many().
            #
            # Serialize and return whatever get_many() returns.
            return serialize(await self.visit.get_many(**query))



Returns
~~~~~~~

The `@returns` decorator takes care of serializing the data returned by the route handler.

*API*

.. automodule:: aioli.controller.decorators
   :noindex:
   :members: returns


*Example – Route handler making use of @takes and @returns*

.. code-block:: python

    from aioli.controller import (
        BaseHttpController, ParamsSchema, RequestProp,
        Method, route, takes, returns
    )

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()

        @route("/", Method.GET, "List of entries")
        @takes(query=ParamsSchema)
        @returns(Visit, many=True)
        async def visits_get(self, query):
            # Transform and validate query params against ParamsSchema,
            # then pass it along to get_many().
            #
            # Transform and dump the object returned from get_many() -
            # according to the Visit schema, as a JSON encoded response
            return await self.visit.get_many(**query)
