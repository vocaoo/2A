import logging

from dataclasses import dataclass

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces import UnitOfWork
from src.application.task.interfaces.persistence import TaskRepo
from src.application.task.interfaces.excel import ExcelProcessor


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UploadFile(Command[None]):
    file: bytes


class UploadFileHandler(CommandHandler[UploadFile, None]):
    def __init__(
        self,
        task_repo: TaskRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
        excel_processor: ExcelProcessor
    ) -> None:
        self._task_repo = task_repo
        self._uow = uow
        self._mediator = mediator
        self._excel_processor = excel_processor

    async def __call__(self, command: UploadFile) -> None:
        file = command.file

        task_list = self._excel_processor.get_tasks_from_excel(file)

        for task in task_list:
            await self._task_repo.add_task(task)
            await self._mediator.publish(task.pull_events())

        await self._uow.commit()

