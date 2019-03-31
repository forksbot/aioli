# -*- coding: utf-8 -*-

from sanic.exceptions import SanicException


class AioliException(SanicException):
    def __init__(self, *args, **kwargs):
        self.log_message = kwargs.pop('write_log', False)

        super(AioliException, self).__init__(*args, **kwargs)
