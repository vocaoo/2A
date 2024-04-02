from dataclasses import dataclass
from typing import Protocol
from uuid import UUID

from src.application.common.pagination import Pagination
from src.application.task.dto import Task, Tasks
from src.domain.common.const import Empty
from src.domain.task.value_objects import StatusState


@dataclass(frozen=True)
class GetTaskFilters:
    deleted: bool | Empty = Empty.UNSET


class TaskReader(Protocol):
    async def get_task_by_id(self, user_id: UUID) -> Task:
        raise NotImplementedError

    async def get_task_by_code(self, code: str) -> Task:
        raise NotImplementedError

    async def get_tasks(
        self,
        filters: GetTaskFilters,
        pagination: Pagination,
        status: StatusState,
    ) -> Tasks:
        raise NotImplementedError
