import logging

from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.task.interfaces.persistence import TaskRepo
from src.domain.task.value_objects import TaskID


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeleteTask(Command[None]):
    task_id: UUID


class DeleteTaskHandler(CommandHandler[DeleteTask, None]):
    def __init__(
        self,
        task_repo: TaskRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
    ) -> None:
        self._task_repo = task_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: DeleteTask) -> None:
        task_id = TaskID(command.task_id)

        task = await self._task_repo.acquire_task_by_id(task_id)
        task.delete_task()

        await self._task_repo.update_task(task)
        await self._mediator.publish(task.pull_events())
        await self._uow.commit()

        logger.info("Task deleted", extra={"task": task})
