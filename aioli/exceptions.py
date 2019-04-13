# -*- coding: utf-8 -*-

from starlette.exceptions import HTTPException


class InternalError(HTTPException):
    def __init__(self, *args, **kwargs):
        super(InternalError, self).__init__(*args, **kwargs)


class AioliException(HTTPException):
    def __init__(self, *args, **kwargs):
        self.log_message = kwargs.pop('write_log', False)

        super(AioliException, self).__init__(*args, **kwargs)
