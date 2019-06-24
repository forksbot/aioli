Info
====

Extensions in Aioli are used for supporting Packages with extra functionality, typically for interacting with remote systems.

To make use of an Extension, the Package itself and its dependencies needs to be registered with the Application.


Create
======

An Extension usually provides an interface with one or more Services. These Services are created using the
:class:`~aioli.service.BaseService` class and often implements the `Factory pattern <https://en.wikipedia.org/wiki/Factory_method_pattern>`_.

Check out the `aioli-rdbms extension <https://github.com/aioli-framework/aioli-rdbms>`_ for an example.


Register
========


An Extension–just like a regular :class:`~aioli.Package`–is registered with the :class:`~aioli.Application`, and
have its Service(s) incorporated into other *Packages* using :meth:`~aioli.service.BaseService.integrate`
or :meth:`~aioli.service.BaseService.connect`.

**Example**

Register the local *users* Package and its dependency, *aioli_rdbms*.

.. code-block:: python

   import aioli_rdbms

   import toml

   from aioli import Application

   import .users

   app = Application(
       config=toml.load("config.toml"),
       packages=[users, aioli_rdbms]
   )




The *aioli_rdbms.Service* can now be attached to *users.UsersService*:

.. code-block:: python

    from aioli import BaseService
    from aioli_rdbms import DatabaseService

    from .database import UserModel

    class UsersService(BaseService):
        db = None

        async def on_startup(self):
            self.db = (
                self.integrate(DatabaseService)
                .use_model(UserModel)
            )

        async def get_one(user_id):
            return await self.db.get_one(pk=user_id)

        ...


Publish
=======

Shortly, a Package Management CLI will be added, along with the
`https://pkgs.aioli.dev <https://pkgs.aioli.dev>`_ website for showing useful info about extension-type *Packages*;
their trust status, install instructions, author and license data, as well as links to source code and more.
