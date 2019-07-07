About
=====

Aioli is a Framework for building RESTful HTTP and WebSocket APIs.
Its easy-to-use component system, which was built with emphasis on portability and composability, offers a sensible separation of application logic, data access and request/response layers.

Furthermore, it makes use of asyncio, is lightweight, and provides high performance and concurrency–especially for IO-bound workloads.

Note that Aioli only works only with modern versions of Python (3.6+) and is *Event loop driven*, i.e. code must be [asynchronous](https://docs.python.org/3/library/asyncio.html).

Not in the mood for reading docs? Check out `The Guestbook Repository <https://github.com/aioli-framework/aioli-guestbook-example>`_ for a comprehensive RESTful HTTP example.

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
   :caption: Extensions

   extensions

.. toctree::
   :caption: Snippets
   :maxdepth: 1

   examples/about
   examples/service/index
   examples/config/index
