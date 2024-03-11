from fastapi import status
from fastapi.exceptions import HTTPException
from core.exceptions.schemas.errors import PydanticError, NotFoundNotificationError


class ValidationHTTPException(HTTPException):
    """Ошибка появления дубликатов в базе данных."""
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, error_schema: PydanticError) -> None:
        """
        Ошибка появления дубликатов в базе данных.
        :param error_schema: Pydantic схема с описанием ошибки
        """
        super().__init__(status_code=self.status_code, detail=error_schema.detail)


class NotFoundHTTPException(HTTPException):
    """Ошибка 'запрашиваемые данные не найдены'"""
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, error_schema: PydanticError = NotFoundNotificationError()) -> None:
        """
        Ошибка 'запрашиваемые данные не найдены'
        :param error_schema: Pydantic схема с описанием ошибки (необязательно)
        """
        super().__init__(status_code=self.status_code, detail=error_schema.detail)
