# -*- coding: utf-8 -*-

from marshmallow import Schema, fields

from aioli.controller import route, schema


async def test_schema_base(mock_request, logger):
    """Using a schema should inject selected parts as arguments"""

    class QuerySchema(Schema):
        p1 = fields.String()

    class RequestSchema(Schema):
        query = fields.Nested(QuerySchema)

    @route('/', 'GET')
    @schema(RequestSchema)
    async def base_schema_handler(_, query):
        assert query['p1'] == 'test'
        return

    req = mock_request(args={'p1': 'test'})
    await base_schema_handler(*req)
