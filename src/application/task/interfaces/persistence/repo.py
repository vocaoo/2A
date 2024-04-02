from abc import abstractmethod
from typing import Protocol

from src.domain.task.entities import Task
from src.domain.task.value_objects import TaskID


class TaskRepo(Protocol):
    @abstractmethod
    async def acquire_task_by_id(self, task_id: TaskID) -> Task:
        raise NotImplementedError

    @abstractmethod
    async def add_task(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, task: Task) -> None:
        raise NotImplementedError
