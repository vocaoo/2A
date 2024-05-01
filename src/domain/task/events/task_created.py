from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class TaskCreated(Event):
    task_id: UUID
    code: str
    name: str
    address: str
    latitude: str | None
    longitude: str | None
    implementer: str | None
    current_indication: float
    previous_indication: float | None
    number: str
    status: str
