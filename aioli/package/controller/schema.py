# -*- coding: utf-8 -*-

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
        super(SchemaOpts, self).__init__(meta, **kwargs)
        self.render_module = JsonSerializer


class Schema(marshmallow.schema.BaseSchema, metaclass=marshmallow.schema.SchemaMeta):
    OPTIONS_CLASS = SchemaOpts


class ParamsSchema(Schema):
    limit = fields.Integer(missing=100, validate=validate.Range(min=0))
    offset = fields.Integer(missing=0, validate=validate.Range(min=0))
    sort = fields.String(missing='')
    query = fields.String(missing='')


class CountSchema(Schema):
    count = fields.Integer()


class DeleteSchema(Schema):
    deleted = fields.Integer()
