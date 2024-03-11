import uuid
import datetime

from typing import Optional

from pydantic import BaseModel

from schemas.base import (BaseNotification, NotificationItem, RetrieveAuditInfo,
                              CreatorAuditInfo, UpdaterAuditInfo, DeleterAuditInfo)


class AdminRetrieveListNotification(BaseNotification):
    """Модель уведомления для получения списка"""
    is_published: bool
    audit_info: Optional[RetrieveAuditInfo] = None

    class Config:
        from_attributes = True


class AdminRetrieveNotification(BaseNotification):
    """Модель уведомления для чтения"""
    audit_info: Optional[RetrieveAuditInfo] = None
    settings: Optional[dict] = None

    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True


class AdminUpdateNotification(BaseModel):
    """Модель уведомления для обновления"""
    item: Optional[NotificationItem] = None
    type: Optional[str] = None

    audit_info: UpdaterAuditInfo
    settings: Optional[dict] = None

    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None


class AdminCreateNotification(BaseModel):
    """Модель уведомления для создания"""
    item: NotificationItem
    type: str

    audit_info: CreatorAuditInfo
    settings: Optional[dict] = None

    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None


class AdminDeleteNotification(BaseModel):
    """Модель уведомления для удаления"""
    audit_info: DeleterAuditInfo
