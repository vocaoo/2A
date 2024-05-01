import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.task.interfaces.persistence import TaskRepo
from src.domain.task.entities import Task
from src.domain.task.value_objects import (
    TaskID,
    Code,
    Name,
    Address,
    Indication,
    Coordinates,
    Implementer,
    Comment,
    Number,
)


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CreateTask(Command[UUID]):
    task_id: UUID
    code: str
    name: str
    address: str
    current_indication: float | None
    implementer: str
    latitude: float | None
    longitude: float | None
    comment: str | None
    number: str | None


class CreateTaskHandler(CommandHandler[CreateTask, TaskID]):
    def __init__(self, task_repo: TaskRepo, uow: UnitOfWork, mediator: EventMediator) -> None:
        self._task_repo = task_repo
        self._uow = uow
        self._mediator = mediator

    async def __call__(self, command: CreateTask) -> UUID:
        task_id = TaskID(command.task_id)
        code = Code(command.code)
        name = Name(command.name)
        address = Address(command.address)
        indication = Indication(current=command.current_indication, previous=None)
        implementer = Implementer(command.implementer)
        coordinates = Coordinates(latitude=command.latitude, longitude=command.longitude)
        comment = Comment(command.comment)
        number = Number(command.number)

        task = Task.create_task(
            task_id=task_id,
            code=code,
            name=name,
            address=address,
            indication=indication,
            implementer=implementer,
            coordinates=coordinates,
            comment=comment,
            number=number,
        )

        await self._task_repo.add_task(task)
        await self._mediator.publish(task.pull_events())
        await self._uow.commit()

        logger.info("Task created", extra={"task": task})

        return command.task_id
