Application
===========

The :class:`aioli.Application` needs to be created with at least one *Package*.
Additional parameters can be provided to further customize the instance - see the docs below for more info.


**API**

.. automodule:: aioli
.. autoclass:: Application
   :members:


.. note::
    The :class:`aioli.Application` and :meth:`aioli.Application.run` can be configured using the environment and files as well.

    *Read more about this in the Configuration section.*


**Example**

.. code-block:: python

    import aioli
    import jet_apispec
    import jet_guestbook

    # Create application
    app = aioli.Application(
        path='/api',
        packages=[
            ('/guestbook', jet_guestbook),
            ('/packages', jet_apispec)
        ]
    )

    # Start server
    app.run(host='192.168.0.1')


