import logging
from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.task.dto import Task
from src.application.task.interfaces.persistence import TaskReader

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetTaskByCode(Query[Task]):
    code: str


class GetTaskByCodeHandler(QueryHandler[GetTaskByCode, Task]):
    def __init__(self, task_reader: TaskReader) -> None:
        self._task_reader = task_reader

    async def __call__(self, query: GetTaskByCode) -> Task:
        task = await self._task_reader.get_task_by_code(query.code)
        logger.debug("Get task by code", extra={"code": query.code, "task": task})
        return task
