from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class TaskCompleted(Event):
    task_id: UUID
    near_photo_url: str
    far_photo_url: str
    latitude: float
    longitude: float
    current_indication: float
    previous_indication: float
    status: str
    completion_date: datetime
