Deploy
======

Development
^^^^^^^^^^^

Given an Application like:

.. code-block:: python

    # File: main.py

    import aioli_guestbook
    import aioli_rdbms

    import toml

    from aioli import Application

    app = Application(
        config=toml.load("config.toml"),
        packages=[
            aioli_guestbook,
            aioli_rdbms,
        ]
    )


...the Aioli CLI can be used to start the Application (using a built-in Uvicorn server).

.. code-block:: bash

    $ python3 -m aioli dev-server main:app



Production
^^^^^^^^^^

Work in progress
