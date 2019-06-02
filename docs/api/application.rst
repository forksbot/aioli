Application
===========

To run the Aioli application, an :class:`~aioli.Application` instance must be created.
Its constructor expects a *list* of at least one :class:`~aioli.Package` to be registered with the application.


.. automodule:: aioli
.. autoclass:: Application


*Example*

.. code-block:: python

    import aioli_guestbook

    from aioli import Application


    app = Application(
        **toml.loads(["config.toml"]),
        debug=False,
        packages=[
            ("/guestbook", aioli_guestbook),
        ]
    )
