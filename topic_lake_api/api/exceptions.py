from fastapi import HTTPException
from starlette import status


class InternalServerError(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=message)


class BadRequest(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class Unauthorized(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


class NotFound(HTTPException):
    def __init__(self, message: str = ''):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
