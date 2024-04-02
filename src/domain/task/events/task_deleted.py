from dataclasses import dataclass
from uuid import UUID

from src.domain.common.events import Event


@dataclass(frozen=True)
class TaskDeleted(Event):
    task_id: UUID
