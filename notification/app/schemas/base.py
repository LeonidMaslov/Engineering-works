import uuid
import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AuditInfoBaseUserData(BaseModel):
    """Модель данных пользователя для `AuditInfo`"""
    name: Optional[str] = Field(None, description="", examples=["Иванов И.И."])
    keycloak_id: Optional[str] = Field(None, examples=[uuid.uuid4()])
    sidecar_id: Optional[str] = Field(None, examples=[""])
    date_time: Optional[str] = Field(alias='date', examples=[datetime.datetime.utcnow()],
                                     default=str(datetime.datetime.utcnow()))


class CreatorAuditInfo(BaseModel):
    """Модель записи `AuditInfo` для создания"""
    creator: AuditInfoBaseUserData


class UpdaterAuditInfo(BaseModel):
    """Модель записи `AuditInfo` для изменения"""
    updater: AuditInfoBaseUserData


class DeleterAuditInfo(BaseModel):
    """Модель записи `AuditInfo` для удаления"""
    deleter: AuditInfoBaseUserData


class RetrieveAuditInfo(BaseModel):
    """Модель `AuditInfo` для чтения"""
    creator: Optional[AuditInfoBaseUserData] = None
    updater: Optional[AuditInfoBaseUserData] = None
    deleter: Optional[AuditInfoBaseUserData] = None


class NotificationItem(BaseModel):
    """Модель контента в уведомлении"""
    title: Optional[str] = None
    description: Optional[str] = None

    url: Optional[str] = None
    button_text: Optional[str] = None
    utm: Optional[str] = None


class BaseNotification(BaseModel):
    """Базовая модель уведомления"""
    id: uuid.UUID
    item: NotificationItem
    type: str
