import uuid

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.dialects.postgresql import UUID


class SQLBaseModel(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4())
