# -*- coding: utf-8 -*-

from starlette.exceptions import HTTPException


class InternalError(HTTPException):
    def __init__(self, *args, **kwargs):
        super(InternalError, self).__init__(*args, **kwargs)


class AioliException(HTTPException):
    def __init__(self, status=500, message='Internal Server Error'):
        super(AioliException, self).__init__(status_code=status, detail=message)


class DatabaseError(HTTPException):
    def __init__(self):
        super(DatabaseError, self).__init__(status_code=500, detail='Database error')


class NoMatchFound(HTTPException):
    def __init__(self, message='Not Found'):
        super(NoMatchFound, self).__init__(status_code=404, detail=message)

