import uuid
from datetime import datetime
from typing import Optional

from pydantic import Field
from fastapi_filter.contrib.sqlalchemy import Filter

from models import Notification


class AdminNotificationFilter(Filter):
    """Набор фильтров для фильтрации уведомлений в административной панели """
    is_published: Optional[bool] = Field(alias="is_published", description="Статус публикации уведомления",
                                         default=True)
    # updated_at: Optional[datetime] = Field(alias="updated_at", description="Дата последнего обновления",
    #                                        examples=[datetime.utcnow()], default=datetime.utcnow())
    # updated_by: Optional[str] = Field(alias="updated_by", description="Пользователь обновивший уведомление",
    #                                   examples=[uuid.uuid4()], default=uuid.uuid4())
    # type: Optional[str] = Field(alias="type", default=None)

    class Constants(Filter.Constants):
        """Таблица для фильтрации"""
        model = Notification

    class Config:
        populate_by_name = True
