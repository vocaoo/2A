import logging
from dataclasses import dataclass

from src.application.common.query import Query, QueryHandler
from src.application.task.dto import Tasks
from src.application.task.interfaces.persistence import TaskReader
from src.domain.user.value_objects import UserID
from src.application.user.interfaces import UserRepo
from src.infrastructure.auth import JWTProcessor


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class GetTasksByUsernameDepartment(Query[Tasks]):
    token: str
    status: str


class GetTasksByUsernameDepartmentHandler(QueryHandler[GetTasksByUsernameDepartment, Tasks]):
    def __init__(self, task_reader: TaskReader, processor: JWTProcessor, user_repo: UserRepo) -> None:
        self._task_reader = task_reader
        self._processor = processor
        self._user_repo = user_repo

    async def __call__(self, query: GetTasksByUsernameDepartment) -> Tasks:
        user_id = UserID(self._processor.decode(query.token))
        user = await self._user_repo.acquire_user_by_id(user_id)
        tasks = await self._task_reader.get_tasks_by_username_and_department(
            username=user.username.to_raw(),
            department=user.department.to_raw(),
            status=query.status,
        )

        logger.info("Get tasks by username and department", extra={
            "username": user.username.to_raw(),
            "department": user.department.to_raw(),
        })

        return tasks
