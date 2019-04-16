# -*- coding: utf-8 -*-

import orm

from aioli.core.manager import DatabaseManager
from aioli.exceptions import DatabaseError, AioliException, NoMatchFound
from .base import BaseService


class DatabaseService(BaseService):
    """Service class providing an interface with common database operations

    :ivar __model__: Peewee.Model
    :ivar db_manager: Aioli database manager (peewee-async)
    """

    __model__: orm.Model
    db_manager: DatabaseManager

    @classmethod
    def register(cls, pkg, mgr):
        super(DatabaseService, cls).register(pkg, mgr)
        cls.db_manager = mgr.db

    @property
    def model(self):
        if not self.__model__:
            raise Exception(f'{self.__class__.__name__}.__model__ not set, unable to perform database operation')

        return self.__model__

    def _model_has_attrs(self, *attrs):
        for attr in attrs:
            if attr not in self.model.fields:
                raise AioliException(400, f'Unknown field {attr}')

        return True

    def _parse_sortstr(self, value: str):
        from sqlalchemy import desc, asc

        if not value:
            return None

        for col_name in value.split(','):
            sort_asc = True
            if col_name.startswith('-'):
                col_name = col_name[1:]
                sort_asc = False

            if self._model_has_attrs(col_name):
                yield asc(col_name) if sort_asc else desc(col_name)

    async def get_many(self, **query):
        sort = query.pop('_sort', None)
        limit = query.pop('_limit', None)
        offset = query.pop('_offset', None)

        query_filtered = (
            self.model.objects.filter(**query)
                .build_select_expression()
                .offset(offset)
                .limit(limit)
                .order_by(*self._parse_sortstr(sort))
        )

        return [o for o in await self.db_manager.database.fetch_all(query_filtered)]

    async def get_one(self, **query):
        try:
            rv = await self.model.objects.get(**query)
            return rv.__dict__
        except (orm.exceptions.MultipleMatches, KeyError) as e:
            self.log.exception(e)
            raise DatabaseError
        except orm.exceptions.NoMatch:
            raise NoMatchFound

    async def create(self, item: dict):
        return await self.model.objects.create(**item)

    async def get_or_create(self, item: dict):
        return await self.db_manager.get_or_create(self.model, **item)

    async def count(self, expression=None, **kwargs):
        query = self._get_query_filtered(expression, **kwargs)
        return await self.db_manager.count(query)

    async def update(self, record, payload):
        if not isinstance(record, peewee.Model):
            record = await self.get_one(record)

        for k, v in payload.items():
            setattr(record, k, v)

        await self.db_manager.update(record)
        return record

    async def delete(self, record_id: int):
        record = await self.get_one(record_id)
        deleted = await self.db_manager.delete(record)
        return {'deleted': deleted}
