from typing import List, Optional

from pydantic import BaseModel


class ValidationErrorMSG(BaseModel):
    """Тело собственной ошибки валидации"""
    loc: list = ["string", 0]
    msg: str = 'string'
    type: str = 'string'


class PydanticError(BaseModel):
    """Схема для собственной ошибки валидации"""
    detail: Optional[List[ValidationErrorMSG]]


class NotFoundNotificationError(PydanticError):
    """Схема ошибки 404"""
    detail: str = "Уведомление не найдено."


class DuplicateNotificationError(PydanticError):
    """Схема ошибки дубликата уведомления"""
    detail: str = "Данное уведомление уже существует"


class NotificationAuditInfoError(PydanticError):
    """Схема ошибки обязательного поля Audit Info"""
    detail: str = "Поле Audit Info не может быть пустым"


class TechnicalWorksDuplicateError(PydanticError):
    detail: str = "Уведомление о технических работах уже существует"
