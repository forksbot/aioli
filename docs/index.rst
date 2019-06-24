About
=====

Aioli is a Framework for building RESTful HTTP and WebSocket API packages, with a sensible separation between request/response handling (transformation, validation, etc), application logic and data access layers.

Furthermore, it makes use of `asyncio <https://docs.python.org/3/library/asyncio.html>`_, is lightweight and provides good performance and concurrency.

Not in mood for reading docs? Check out the `The Guestbook example <https://github.com/aioli-framework/aioli-guestbook-example>`_: a Comprehensive RESTful HTTP API
package.

.. toctree::
   :caption: Setup

   setup/install
   setup/configure
   setup/deploy

.. toctree::
   :caption: Build

   api/application
   api/package
   api/config
   api/controller/index
   api/service

.. toctree::
   :caption: Extend

   extensions

.. toctree::
   :caption: Examples
   :maxdepth: 1

   examples/about
   examples/service/index
   examples/config/index
