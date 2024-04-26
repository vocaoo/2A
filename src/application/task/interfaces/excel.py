from abc import ABC, abstractmethod

from src.domain.task.entities import Task


class ExcelProcessor(ABC):

    @abstractmethod
    def get_tasks_from_excel(self, workbook: bytes) -> list[Task]:
        raise NotImplementedError

    @abstractmethod
    def get_file_from_database(self, tasks: list) -> bytes:
        raise NotImplementedError
