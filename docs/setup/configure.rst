Configure
=========

Configuration can be done by either using environment variables, or a dictionary provided to the Aioli Application.



Mappings
~~~~~~~~

===================   =======================  ===========
Constructor           Environment              DEFAULT
===================   =======================  ===========
listen_host           AIOLI_LISTEN_HOST        127.0.0.1
listen_port           AIOLI_LISTEN_PORT        5000
debug                 AIOLI_DEBUG              False
workers               AIOLI_WORKERS            [cores] * 2
api_base              AIOLI_API_BASE           /api
db_url                AIOLI_DB_URL             None
concurrency           AIOLI_MAX_CONCURRENCY    None
limit_requests        AIOLI_MAX_REQUESTS       None
timeout_keepalive     AIOLI_TIMEOUT_KEEPALIVE  None
===================   =======================  ===========


Environment
~~~~~~~~~~~

Configuring Aioli using environment variables can be useful in containerized environments.

.. code-block:: shell

   $ export AIOLI_LISTEN_HOST="0.0.0.0"
   $ export AIOLI_LISTEN_PORT="5555"


.. _app-constructor-label:

Constructor
~~~~~~~~~~~

The configuration can be provided as keyword arguments directly to the :class:`aioli.Application` constructor.

.. code-block:: python

   import aioli

   app = aioli.Application(
       **toml.loads(["config.toml"]),
       debug=False,
       packages=[...]
       ...
   )


Access
~~~~~~

The configuration is available as a Dictionary in :attr:`Controller.config` and :attr:`Service.config`.

