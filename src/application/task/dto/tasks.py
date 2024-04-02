from typing import TypeAlias

from src.application.common.pagination import PaginatedItemsDTO


from .deleted_task import DeletedTask
from .task import Task


TasksDTOs: TypeAlias = Task | DeletedTask
Tasks: TypeAlias = PaginatedItemsDTO[TasksDTOs]
