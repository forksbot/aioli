About
=====

To make use of a third-party Aioli Package, the Package itself and its dependencies needs to be explicitly registered with the Application.

The typical Aioli extension-type *Package* manages one or more :ref:`service-docs` objects, provides an API of its own, and may contain :ref:`controller-docs` code as well.


Create
======

Extensions make use of the :class:`~aioli.service.BaseService` class and
usually implements the `Factory pattern <https://en.wikipedia.org/wiki/Factory_method_pattern>`_
teamed by the :meth:`~aioli.service.BaseService.integrate` method.

Check out the `aioli-rdbms extension <https://github.com/aioli-framework/aioli-rdbms>`_ for an example.


Use
===


Extensions are registered with the :class:`~aioli.Application`, just like a regular :class:`~aioli.Package`–
and usually have their Services incorporated into other *Packages*.

**Example**

Register the local *users* Package and its dependency, *aioli_rdbms*.

.. code-block:: python

    import aioli_rdbms

    from .packages import users

    app = Application(
        packages=[
            ("/users", users),
            (None, aioli_rdbms),
            ...
        ]
    )




The *aioli_rdbms.Service* can now be attached to *users.UsersService*:

.. code-block:: python

    from aioli import BaseService
    from aioli_rdbms import DatabaseService

    from .database import UserModel

    class UsersService(BaseService):
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
