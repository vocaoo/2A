from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from src.domain.task.value_objects import StatusState

from .base import TimedBaseModel


class Task(TimedBaseModel):
    __tablename__ = "tasks"
    __mapper_args__ = {"eager_defaults": True}

    task_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid7)
    code: Mapped[str]
    name: Mapped[str | None]
    address: Mapped[str]
    current_indication: Mapped[float]
    previous_indication: Mapped[float | None] = mapped_column(default=None)
    implementer: Mapped[str]
    latitude: Mapped[float | None] = mapped_column(default=None)
    longitude: Mapped[float | None] = mapped_column(default=None)
    comment: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[StatusState]
    near_photo_url: Mapped[str | None] = mapped_column(default=None)
    far_photo_url: Mapped[str | None] = mapped_column(default=None)
    completion_date: Mapped[datetime | None] = mapped_column(default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)
