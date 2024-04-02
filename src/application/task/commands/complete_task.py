import logging

from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.task.interfaces.persistence import TaskRepo
from src.application.common.interfaces import UnitOfWork
from src.application.task.interfaces.object_storage import ObjectStorage
from src.application.task.interfaces.metadata import PhotoMetadataProcessor
from src.domain.task.value_objects import TaskID, PhotoURL, Indication


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class CompleteTask(Command[None]):
    task_id: UUID
    near_photo_url: str
    far_photo_url: str
    previous_indication: float
    current_indication: float


class CompleteTaskHandler(CommandHandler[CompleteTask, None]):
    def __init__(
        self,
        task_repo: TaskRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
        object_storage: ObjectStorage,
        metadate_processor: PhotoMetadataProcessor,
    ) -> None:
        self._task_repo = task_repo
        self._uow = uow
        self._mediator = mediator
        self._object_storage = object_storage
        self._metadate_processor = metadate_processor

    async def __call__(self, command: CompleteTask) -> None:
        task_id = TaskID(command.task_id)
        photo_url = PhotoURL(command.near_photo_url, command.far_photo_url)
        indication = Indication(command.current_indication, command.previous_indication)

        photo = self._object_storage.get(command.near_photo_url)
        coordinates = self._metadate_processor.get_coordinates(photo)

        task = await self._task_repo.acquire_task_by_id(task_id)
        task.complete_task(photo_url, indication, coordinates)

        await self._task_repo.update_task(task)
        await self._mediator.publish(task.pull_events())
        await self._uow.commit()

        logger.info("Task completed", extra={"task": task})
