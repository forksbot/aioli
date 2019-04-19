from orm import models
import databases
import sqlalchemy


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


class BaseModelMeta(models.ModelMetaclass):
    def __new__(mcs, name, bases, attrs):
        if '__tablename__' in attrs:
            assert '__module__' in attrs

            pkg_name = attrs['__module__'].split('.')[0]
            attrs['__tablename__'] = f"{pkg_name}__{attrs['__tablename__']}"

        attrs['__metadata__'] = DatabaseManager.metadata

        new_model = super(BaseModelMeta, mcs).__new__(  # type: ignore
            mcs, name, bases, attrs
        )

        return new_model


class BaseModel(models.Model, metaclass=BaseModelMeta):
    __abstract__ = True
    __metadata__ = None
