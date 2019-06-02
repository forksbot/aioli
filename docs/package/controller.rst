


Routing
*******

Routing is implemented using one or more *handlers* decorated with a `@route`.
Used without the `@input_load` decorator, the entire request object is passed to the handler.

**API**

.. automodule:: aioli.controller.decorators
   :members: route

**Example**

.. code-block:: python

    from aioli.utils import jsonify
    from aioli.controller import BaseController, route

    class Controller(BaseController):
        async def on_request(self, request):
            self.log.debug(f'Request received: {request}')

        @route('/<name>', 'GET'):
        async def greet(self, request, name):
            return jsonify({'msg': f'hello {name} from {request.ip}')


Transformation
**************

Request and response transformation is performed when a request reaches `@input_load`,
and upon handler return in `@output_dump`. These two decorators provides a declarative way of defining
what comes in and what goes out of a route handler.

**API**

.. automodule:: aioli.controller.decorators
   :members: input_load, output_dump

**Example of request/response transformation**

.. code-block:: python

    from aioli.controller import BaseController, route
    from aioli.schema import ParamsSchema
    from .visit import svc_visit
    from .visit.schemas import Visit

    class Controller(BaseController):
        async def on_request(self, request):
            self.log.debug(f'Request received: {request}')

        @route('/', 'GET')
        @input_load(query=ParamsSchema)  # Transform and validate the query string
        @output_dump(Visit, many=True)  # Dump many `Visit`s
        async def visits_get(self, query):
            # Call the service layer and dump the result as a JSON string
            return await svc_visit.get_many(**query)

        @route('/<visit_id>', 'PUT')  # Perform an update operation
        @input_load(body=Visit)  # Transform and validate the JSON payload
        @output_dump(Visit)  # Dump one `Visit`
        async def visit_update(self, remote_addr, body, visit_id):
            # Call the service layer and dump the result as a JSON string
            return await svc_visit.visit_update(remote_addr, visit_id, body)


Schemas
*******

Schemas are used in transformation decorators to perform object serialization and generating HTTP API documentation.

**Example**

.. code-block:: python

    from aioli.schema import fields, Schema


    class Visit(Schema):
        id = fields.Integer()
        visited_on = fields.String(attribute='created_on')
        message = fields.String()
        name = fields.String()

        class Meta:
            dump_only = ['id', 'visited_on']
            load_only = ['visit_id', 'visitor_id']


    class VisitNew(Schema):
        message = fields.String(required=True)
        name = fields.String(required=True)


.. seealso::
   Check out the
   `Marshmallow API docs <https://marshmallow.readthedocs.io/en/latest/api_reference.html>`_
   for more info on how to work with schemas.


