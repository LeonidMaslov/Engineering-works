import pytz
import datetime

from sqlalchemy import JSON, DateTime, Boolean, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from models import SQLBaseModel


class Notification(SQLBaseModel):
    """Модель таблицы `Notification`"""
    __tablename__ = "notifications"

    item: Mapped[dict] = mapped_column(JSON)

    start_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    type: Mapped[str] = mapped_column(String(length=128))

    audit_info: Mapped[dict] = mapped_column(JSON, nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def is_published(self) -> bool:
        now = datetime.datetime.utcnow()
        if self.end_date:
            return self.start_date <= pytz.utc.localize(now) <= self.end_date
        return self.start_date <= now
