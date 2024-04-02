import logging
from dataclasses import dataclass

from src.application.common.pagination.dto import Pagination
from src.application.common.query import Query, QueryHandler
from src.application.task.dto import Tasks
from src.application.task.interfaces.persistence import TaskReader, GetTaskFilters
from src.domain.task.value_objects import StatusState

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetTasks(Query[Tasks]):
    filters: GetTaskFilters
    pagination: Pagination
    status: StatusState


class GetTasksHandler(QueryHandler[GetTasks, Tasks]):
    def __init__(self, task_reader: TaskReader) -> None:
        self._task_reader = task_reader

    async def __call__(self, query: GetTasks) -> Tasks:
        tasks = await self._task_reader.get_tasks(query.filters, query.pagination, query.status)
        logger.debug("Get tasks", extra={
            "tasks": tasks,
            "pagination": query.pagination,
            "filters": query.filters
        })
        return tasks
