import ujson
import marshmallow

from marshmallow import validate
from marshmallow import *


class JsonSerializer:
    @staticmethod
    def loads(data, **kwargs):
        return ujson.loads(data, **kwargs)

    @staticmethod
    def dumps(data, **kwargs):
        return ujson.dumps(data, **kwargs)


class SchemaOpts(marshmallow.schema.SchemaOpts):
    def __init__(self, meta, **kwargs):
        self.load_only = []
        self.dump_only = []

        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = JsonSerializer
        self.unknown = "EXCLUDE"


class Schema(marshmallow.schema.Schema):
    OPTIONS_CLASS = SchemaOpts


class HttpParams(Schema):
    limit = fields.Integer(missing=100, validate=validate.Range(min=0))
    offset = fields.Integer(missing=0, validate=validate.Range(min=0))
    sort = fields.String(missing="")
    query = fields.String(missing="")


class HttpHeader(Schema):
    host = fields.String()
    user_agent = fields.String(data_key="user-agent")


class Count(Schema):
    count = fields.Integer()
