from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class TaskRejected(Event):
    task_id: UUID
    current_indication: float
    status: str
