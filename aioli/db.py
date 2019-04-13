from orm.models import Model, ModelMetaclass
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


class BaseModelMeta(ModelMetaclass):
    def __new__(mcs, name, bases, attrs):
        attrs['__metadata__'] = DatabaseManager.metadata

        new_model = super(BaseModelMeta, mcs).__new__(  # type: ignore
            mcs, name, bases, attrs
        )

        return new_model


class BaseModel(Model, metaclass=BaseModelMeta):
    __abstract__ = True
    __metadata__ = None

    @classmethod
    def register(cls, pkg_name):
        cls.__tablename__ = f'{pkg_name}__{cls.__tablename__}'
        cls.__database__ = DatabaseManager.database

        pkname = None
        columns = []
        for name, field in cls.fields.items():
            if field.primary_key:
                pkname = name

            columns.append(field.get_column(name))

        cls.__table__ = sqlalchemy.Table(cls.__tablename__, cls.__metadata__, *columns)
        cls.__table__.__pkname__ = pkname
