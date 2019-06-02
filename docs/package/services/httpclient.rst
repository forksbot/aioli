HttpClientService
=================

The built-in :class:`~aioli.service.HttpClientService` provides
an interface for interacting with HTTP servers.

Example
*******

.. code-block:: python

    from aioli.service import HttpClientService, DatabaseService

    from .model import EntryModel

    class EntryService(HttpClientService, DatabaseService):
        __model__ = EntryModel

        def __init__(self):
            self.backup_url = 'https://192.168.1.10'

        async def entry_add(self, entry_new):
            entry = await self.create(entry_new)

            self.log.info(f'sending a copy to {self.backup_url}')
            await self.http_post(self.backup_url, entry_new)

            return entry


API
***

.. automodule:: aioli.service
.. autoclass:: HttpClientService
   :members:

