# -*- coding: utf-8 -*-

from os import environ as env
from multiprocessing import cpu_count
from marshmallow import Schema, fields


class CoreSchema(Schema):
    listen_host = fields.String(missing="127.0.0.1")
    listen_port = fields.Integer(missing=5000)
    debug = fields.Bool(missing=False)
    workers = fields.Integer(missing=cpu_count() * 2)
    db_url = fields.String(missing=None)
    path = fields.String(missing="/api", attribute="api_base")


class ConfigConsumer:
    def __init__(self, consumables):
        self.consumables = consumables

    @property
    def consumed(self):
        schema = CoreSchema()
        params = {}

        for key, field in CoreSchema._declared_fields.items():
            if key in env:  # Prefer environ
                value = env.get(key)
                if isinstance(field, fields.Integer):
                    value = int(value)
                if isinstance(field, fields.Boolean):
                    value = str(value).strip().lower() in ["1", "true", "yes"]

                params[key] = value
            elif key in self.consumables:
                params[key] = self.consumables.pop(key)

        return schema.load(params)
