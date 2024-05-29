from collections.abc import Iterable
from uuid import UUID

from sqlalchemy import func, select, literal, or_

from src.application.task.dto import Tasks
from src.application.task.interfaces.persistence import TaskReader, TaskRepo, GetTaskFilters
from src.domain.common.const import Empty
from src.application.common.pagination import Pagination, PaginationResult, SortOrder
from src.application.task import dto
from src.domain.task.value_objects import StatusState, TaskID
from src.infrastructure.database.models import Task
from src.infrastructure.database.converters.task import (
    convert_db_model_to_active_task_dto,
    convert_db_model_to_task_dto,
    convert_db_model_to_task_entity,
    convert_task_entity_to_db_model,
)
from src.infrastructure.database.exception_mapper import exception_mapper

from .base import SQLAlchemyRepo


class TaskReaderImpl(SQLAlchemyRepo, TaskReader):
    @exception_mapper
    async def get_task_by_id(self, task_id: UUID) -> dto.TasksDTOs:
        task: Task | None = await self._session.scalar(
            select(Task).where(Task.task_id == task_id)
        )
        if task is None:
            raise

        return convert_db_model_to_task_dto(task)

    @exception_mapper
    async def get_task_by_code(self, code: str) -> dto.Task:
        task: Task | None = await self._session.scalar(
            select(Task).where(Task.code == code)
            .where(Task.status == StatusState.EXECUTING)
        )
        if task is None:
            raise

        return convert_db_model_to_active_task_dto(task)

    async def get_tasks(
        self,
        filters: GetTaskFilters,
        pagination: Pagination,
        status: StatusState,
    ) -> dto.Tasks:
        query = select(Task)

        if pagination.order is SortOrder.ASC:
            query = query.order_by(Task.task_id.desc())
        else:
            query = query.order_by(Task.task_id.asc())

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Task.deleted_at.is_not(None))
            else:
                query = query.where(Task.deleted_at.is_(None))

        query = query.where(Task.status == status)

        # if pagination.offset is not Empty.UNSET:
        #     query = query.offset(pagination.offset)
        # if pagination.limit is not Empty.UNSET:
        #     query = query.limit(pagination.limit)

        result: Iterable[Task] = await self._session.scalars(query)
        tasks = [convert_db_model_to_task_dto(task) for task in result]
        tasks_count = await self._get_tasks_count(filters)
        return dto.Tasks(
            data=tasks,
            pagination=PaginationResult.from_pagination(pagination, total=tasks_count),
        )

    async def get_tasks_by_username_and_department(
        self,
        username: str,
        department: str,
        status: str,
    ) -> Tasks:
        query = select(Task).filter(or_(
            Task.implementer == username,
            Task.code.like(f"{department}%")
        )).filter(Task.status == status)
        result: Iterable[Task] = await self._session.scalars(query)
        tasks = [convert_db_model_to_task_dto(task) for task in result]
        return tasks

    async def _get_tasks_count(self, filters: GetTaskFilters) -> int:
        query = select(func.count(Task.task_id))

        if filters.deleted is not Empty.UNSET:
            if filters.deleted:
                query = query.where(Task.deleted_at.is_not(None))
            else:
                query = query.where(Task.deleted_at.is_(None))

        tasks_count: int = await self._session.scalar(query)
        return tasks_count


class TaskRepoImpl(SQLAlchemyRepo, TaskRepo):
    async def acquire_task_by_id(self, task_id: TaskID) -> Task:
        task: Task | None = await self._session.get(
            Task, task_id.to_raw(), with_for_update=True
        )
        if task is None:
            raise

        return convert_db_model_to_task_entity(task)

    async def add_task(self, task: Task) -> None:
        db_user = convert_task_entity_to_db_model(task)
        self._session.add(db_user)
        await self._session.flush((db_user,))

    async def update_task(self, task: Task) -> None:
        db_user = convert_task_entity_to_db_model(task)
        await self._session.merge(db_user)

    async def get_tasks_uuid(self) -> list[UUID]:
        query = select(Task.task_id)
        result = await self._session.execute(query)
        return [task_id[0] for task_id in result.fetchall()]
