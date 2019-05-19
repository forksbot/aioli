# -*- coding: utf-8 -*-

import databases
import sqlalchemy

from orm import models


class DatabaseManager:
    engine = None
    url = None
    database: databases.Database = None
    metadata = sqlalchemy.MetaData()

    @classmethod
    async def init(cls, url):
        cls.url = str(url)
        cls.database = databases.Database(cls.url)
        await cls.database.connect()
        return cls()


class ModelMeta(models.ModelMetaclass):
    def __new__(mcs, name, bases, attrs):
        if '__tablename__' in attrs:
            assert '__module__' in attrs

            pkg_name = attrs['__module__'].split('.')[0]
            attrs['__tablename__'] = f"{pkg_name}__{attrs['__tablename__']}"

        attrs['__metadata__'] = DatabaseManager.metadata
        return super(ModelMeta, mcs).__new__(mcs, name, bases, attrs)


class Model(models.Model, metaclass=ModelMeta):
    __abstract__ = True
    __metadata__ = None
