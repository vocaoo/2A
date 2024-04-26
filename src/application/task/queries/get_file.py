import logging
from dataclasses import dataclass

from src.application.common.pagination.dto import Pagination
from src.application.common.query import Query, QueryHandler
from src.application.task.dto import Tasks
from src.application.task.interfaces.persistence import TaskReader, GetTaskFilters
from src.domain.task.value_objects import StatusState
from src.application.task.interfaces.excel import ExcelProcessor

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetFile(Query[bytes]):
    filters: GetTaskFilters
    pagination: Pagination
    status: StatusState


class GetFileHandler(QueryHandler[GetFile, bytes]):
    def __init__(self, task_reader: TaskReader, excel_processors: ExcelProcessor) -> None:
        self._task_reader = task_reader
        self._excel_processors = excel_processors

    async def __call__(self, query: GetFile) -> Tasks:
        tasks = await self._task_reader.get_tasks(query.filters, query.pagination, query.status)
        file = self._excel_processors.get_file_from_database(tasks.data)

        logger.debug("Get tasks", extra={
            "tasks": tasks,
            "pagination": query.pagination,
            "filters": query.filters
        })
        return file
