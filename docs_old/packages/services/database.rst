.. _db_service:

DatabaseService
===============

The built-in :class:`~aioli.service.DatabaseService` inherits from :class:`~aioli.service.BaseService` and
provides an interface for interacting with MySQL and PostgreSQL databases using the
`peewee-async manager <https://peewee-async.readthedocs.io/en/latest/peewee_async/api.html#manager>`_.

Example
*******

.. code-block:: python

    from aioli.service import DatabaseService
    from aioli.exceptions import AioliException

    from aioli_guestbook.model import VisitModel

    class VisitService(DatabaseService):
        __model__ = VisitModel

        async def get_authored(self, visit_id, remote_addr):
            visit = await self.get_by_pk(visit_id)
            if visit.visitor.ip_addr != remote_addr:
                raise AioliException('Not allowed from your IP', 403)

            return visit

        async def visit_count(self, ip_addr):
            return await self.count(VisitModel.visitor.ip_addr == ip_addr)

API
***

.. automodule:: aioli.service
.. autoclass:: DatabaseService
   :members:


.. important::
   The `__model__` class attribute must be set for Services implementing the *DatabaseService*.


Models
******

Models are implemented using `Peewee.Model <http://docs.peewee-orm.com/en/latest/peewee/models.html>`_.

Example
^^^^^^^

.. code-block:: python

    from datetime import datetime
    from peewee import Model, ForeignKeyField, CharField, DateTimeField
    from .visitor import VisitorModel


    class VisitModel(Model):
        class Meta:
            table_name = 'visit'

        created_on = DateTimeField(default=datetime.now)
        message = CharField(null=False)
        visitor = ForeignKeyField(VisitorModel)

        @classmethod
        def extended(cls, *fields):
            return cls.select(VisitModel, VisitorModel, *fields).join(VisitorModel)
