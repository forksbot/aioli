HttpController
==============

Creating an HTTP API interface – be it RESTful or otherwise – is done using the
:class:`~aioli.controller.BaseHttpController` class.


**API**

.. automodule:: aioli.controller
.. autoclass:: BaseHttpController
   :members: on_ready, on_request


*Example*

.. code-block:: python

    from aioli.controller import BaseHttpController

    from .service import VisitService


    class HttpController(BaseHttpController):
        def __init__(self):
            self.visit = VisitService()
            self.log.debug("Guestbook opening")

        async def on_ready(self):
            self.log.debug(f"Guestbook opened at {self.pkg.path}")

        async def on_request(self, request):
            self.log.debug(f"Request received: {request}")


Routing
-------

Route handlers are standard Python methods decorated with the `@route`.

**API**

.. automodule:: aioli.controller.decorators
   :members: route

*Example*

.. code-block:: python

    from aioli.controller import BaseHttpController, Method, route

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()
            self.log.debug("Guestbook opening")

        async def on_ready(self):
            self.log.debug(f"Guestbook opened at {self.pkg.path}")

        async def on_request(self, request):
            self.log.debug(f"Request received: {request}")

        @route("/", Method.GET, "List of entries")
        async def visits_get(self, request):
            # Just pass along the query params
            return await self.visit.get_many(**request.query_params)


Transformation
--------------

Transformation is implemented on route handlers using `@takes` and `@returns`. These decorators offer
a simple yet powerful way of shaping and validating request data, while also making sure API endpoints
only returns expected data.


Takes
~~~~~

The `@takes` decorator accepts

**API**

.. automodule:: aioli.controller.decorators
   :members: takes

*Example*

.. code-block:: python

    from aioli.controller import (
        BaseHttpController, ParamsSchema, RequestProp,
        Method, route, takes
    )

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()
            self.log.debug("Guestbook opening")

        async def on_ready(self):
            self.log.debug(f"Guestbook opened at {self.pkg.path}")

        async def on_request(self, request):
            self.log.debug(f"Request received: {request}")

        @route("/", Method.GET, "List of entries")
        @takes(query=ParamsSchema)
        async def visits_get(self, query):
            return await self.visit.get_many(**query)




Returns
~~~~~~~

**API**

.. automodule:: aioli.controller.decorators
   :members: returns


*Example*

.. code-block:: python

    from aioli.controller import (
        BaseHttpController, ParamsSchema, RequestProp,
        Method, route, takes, returns
    )

    from .service import VisitService


    class Controller(BaseController):
        def __init__(self):
            self.visit = VisitService()
            self.log.debug("Guestbook opening")

        async def on_ready(self):
            self.log.debug(f"Guestbook opened at {self.pkg.path}")

        async def on_request(self, request):
            self.log.debug(f"Request received: {request}")

        @route("/", Method.GET, "List of entries")
        @takes(query=ParamsSchema)
        @returns(Visit, many=True)
        async def visits_get(self, query):
            return await self.visit.get_many(**query)

