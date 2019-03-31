About
=====

The idea with Aioli is to provide developers with a sensible base
structure and set of tools for building *performant*, *lightweight* and
*scalable* HTTP API packages that can be easily deployed or distributed.

It’s built on top of `aiohttp`_ and uses the *blazing fast* `uvloop`_
implementation of the asyncio event loop.

Features and limitations:

- Delivers performance and concurrency
- Scales horizontally
- Supports CORS and JWT out of the box
- Has built-in support for `Postgres`_ databases
- Provides intuitive tools for object serialization
- Created with `Docker`_ and `Kubernetes`_ in mind
- Works only with modern versions of Python (3.6+)
- Event loop driven; code must be `asynchronous`_

.. _aiohttp: https://github.com/aio-libs/aiohttp
.. _uvloop: https://github.com/MagicStack/uvloop
.. _Postgres: https://www.postgresql.org
.. _Docker: https://www.docker.com
.. _Kubernetes: https://kubernetes.io
.. _asynchronous: https://docs.python.org/3/library/asyncio.html

.. toctree::
   :hidden:

   self

.. toctree::
   :caption: General

   general


.. toctree::
   :caption: Configuration

   config/environment
   config/instance
   config/file

.. toctree::
   :caption: Core

   core/application
   core/manager

.. toctree::
   :caption: Packages

   packages/definition
   packages/controller
   packages/services/index
