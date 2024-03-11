import datetime
from typing import Optional

from schemas.base import BaseNotification


class UserNotification(BaseNotification):
    start_date: datetime.datetime
    end_date: Optional[datetime.datetime] = None

    settings: Optional[dict] = None

    class Config:
        from_attributes = True
