# -*- coding: utf-8 -*-

from enum import Enum

import orm

from sqlalchemy import select, func, desc, asc, text, sql

from aioli.db import Model
from aioli.manager import DatabaseManager
from aioli.exceptions import AioliException, NoMatchFound


class FilterOperator(Enum):
    EXACT = "__eq__"
    IEXACT = "ilike"
    CONTAINS = "like"
    ICONTAINS = "ilike"
    IN = "in_"
    GT = "__gt__"
    GTE = "__ge__"
    LT = "__lt__"
    LTE = "__le__"


class DatabaseService:
    """Service class providing an interface for common database operations"""

    def __init__(self, manager: DatabaseManager, model: Model):
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
    def objects_joined(self):
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

        for colname in value.split(','):
            sort_asc = True
            if colname.startswith('-'):
                colname = colname[1:]
                sort_asc = False

            if self._model_has_attrs(colname):
                # @TODO - add support for ordering by related fields
                tbl_colname = text(f'{self.model.__tablename__}.{colname}')
                yield asc(tbl_colname) if sort_asc else desc(tbl_colname)

    def _parse_query(self, **kwargs):
        # @TODO - implement _model_has_attrs for local and referenced values
        # @TODO - split up method, reuse in _parse_sortstr

        clauses = []

        for key, value in kwargs.items():
            if "__" in key:
                parts = key.split("__")

                op = parts[-1].upper()
                field_name = parts[-2]
                related_tbl = parts[:-2]

                if len(related_tbl) > 1:
                    raise AioliException(message="Unsupported query depth", status=400)
                elif len(related_tbl) == 1:
                    model = self.model.fields.get(related_tbl[0]).to
                    column = model.__table__.columns[field_name]
                else:
                    column = self.model.__table__.columns[field_name]
            else:
                op = FilterOperator.EXACT
                column = self.model.__table__.columns[key]

            try:
                op_attr = FilterOperator[op].value
            except KeyError:
                raise AioliException(
                    message=f"Invalid operator: {op}, available: {[e.name for e in FilterOperator]}",
                    status=400
                )

            if isinstance(value, Model):
                value = value.pk
            elif op in [FilterOperator.CONTAINS.name, FilterOperator.ICONTAINS.name]:
                value = "%" + value + "%"

            clause = getattr(column, op_attr)(value)
            clauses.append(clause)

        if clauses:
            if len(clauses) == 1:
                return clauses[0]
            else:
                return sql.and_(*clauses)

        return None

    async def get_many(self, query=None, sort=None, limit=None, offset=None):
        stmt = self.objects_joined.build_select_expression().limit(limit).offset(offset)

        if query:
            clauses = dict([clause.split('=') for clause in query.split(',')])
            stmt = stmt.where(self._parse_query(**clauses))

        if sort:
            sort_fields = self._parse_sortstr(sort)
            stmt = stmt.order_by(*sort_fields)

        return [
            self.model.from_row(row, select_related=self.relations)
            for row in await self.manager.database.fetch_all(stmt)
        ]

    async def get_one(self, load_related=True, **kwargs) -> any:
        try:
            if load_related:
                return await self.objects_joined.get(**kwargs)

            return await self.objects.get(**kwargs)
        except (orm.exceptions.MultipleMatches, KeyError) as e:
            raise AioliException(e)
        except orm.exceptions.NoMatch:
            raise NoMatchFound

    async def create(self, **item: dict):
        return await self.model.objects.create(**item)

    async def count(self, **kwargs):
        clauses = self._parse_query(**kwargs)
        query = select([func.count()]).select_from(self.model.__table__).where(clauses)
        return await self.manager.database.fetch_val(query)

    async def update(self, record, payload):
        pass

    async def delete(self, record_id: int):
        pass
