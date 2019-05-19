# -*- coding: utf-8 -*-

import orm

from sqlalchemy import select, func, desc, asc

from aioli.manager import DatabaseManager
from aioli.exceptions import AioliException, NoMatchFound


class DatabaseService:
    """Service class providing an interface for common database operations"""

    manager: DatabaseManager

    def __init__(self, manager, model):
        self.model = model
        self.relations = self._get_relations()
        self.manager = manager

    def _get_relations(self):
        relations = []
        for name, field in self.model.fields.items():
            if not isinstance(field, orm.fields.ForeignKey):
                continue

            relations.append(name)

        return relations

    @property
    def extended(self):
        if self.relations:
            return self.objects.select_related(self.relations)

        return self.objects

    @property
    def objects(self):
        return self.model.objects

    def _model_has_attrs(self, *attrs):
        for attr in attrs:
            if attr not in self.model.fields:
                raise AioliException(400, f'Unknown field {attr}')

        return True

    def _parse_sortstr(self, value: str):
        if not value:
            return None

        for col_name in value.split(','):
            sort_asc = True
            if col_name.startswith('-'):
                col_name = col_name[1:]
                sort_asc = False

            if self._model_has_attrs(col_name):
                yield asc(col_name) if sort_asc else desc(col_name)

    async def get_many(self, **params):
        sort = self._parse_sortstr(params.pop('_sort', None))
        limit = params.pop('_limit', None)
        offset = params.pop('_offset', None)

        return await self.extended.filter(**params).limit(limit).all()

    async def get_one(self, load_related=True, **query):
        try:
            if load_related:
                return await self.extended.get(**query)

            return await self.objects.get(**query)
        except (orm.exceptions.MultipleMatches, KeyError) as e:
            raise AioliException(e)
        except orm.exceptions.NoMatch:
            raise NoMatchFound

    async def create(self, **item: dict):
        return await self.model.objects.create(**item)

    async def count(self, **params):
        # query = self.model.objects.filter()
        # query = select([func.count()], **params).select_from(self.model.__table__)
        #query = select([func.count()]).select_from(self.model.__table__)
        #return await self.manager.database.fetch_val(query)
        query = self.extended.filter(**params)
        # return await query.count()
        return 0

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
