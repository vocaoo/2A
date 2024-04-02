import logging

from dataclasses import dataclass
from uuid import UUID

from src.application.common.query import Query, QueryHandler
from src.application.task.dto import Task
from src.application.task.interfaces.persistence import TaskReader


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetTaskByID(Query[Task]):
    task_id: UUID


class GetTaskByIDHandler(QueryHandler[GetTaskByID, Task]):
    def __init__(self, task_reader: TaskReader) -> None:
        self._task_reader = task_reader

    async def __call__(self, query: GetTaskByID) -> Task:
        task = await self._task_reader.get_task_by_id(query.task_id)
        logger.info("Get task by ID", extra={"task_id": query.task_id, "task": task})
        return task
