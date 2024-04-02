from dataclasses import dataclass
from uuid import UUID

from src.domain.common.exceptions import DomainException


@dataclass(eq=True)
class TaskIsDeleted(RuntimeError, DomainException):
    task_id: UUID

    @property
    def title(self) -> str:
        return f'The task with "{self.task_id}" task_id is deleted'
