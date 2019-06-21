.. _service-docs:

Service
=======

The Service layer typically takes care of interacting with external applications: Databases, Remote Web APIs, Message Queues, etc.

Services can be connected and–to provide a good level of flexibility–supports both Inheritance and two types of Composition.

Check out the :ref:`service-to-service-example` example to see how a service can integrate and interact with other services.

.. automodule:: aioli.service
.. autoclass:: BaseService
   :members: on_startup, on_shutdown, integrate, connect

