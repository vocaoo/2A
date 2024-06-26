from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.application.common.dto import DTO


@dataclass(frozen=True)
class Task(DTO):
    task_id: UUID
    code: str
    name: str
    address: str
    current_indication: float
    previous_indication: float
    implementer: str
    latitude: float | None
    longitude: float | None
    comment: str
    status: str
    near_photo_url: str
    far_photo_url: str
    number: str | None
    completion_date: datetime
    deleted_at: None = field(default=None, init=False)
