# -*- coding: utf-8 -*-

import typesystem


class ParamsSchema(typesystem.Schema):
    _limit = typesystem.Integer(minimum=0)
    _offset = typesystem.Integer(minimum=0)
    _sort = typesystem.String(default='')


class CountSchema(typesystem.Schema):
    count = typesystem.Integer()


class DeleteSchema(typesystem.Schema):
    deleted = typesystem.Integer()
