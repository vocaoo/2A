from dataclasses import dataclass
from enum import Enum

from src.domain.common.value_objects import ValueObject


class StatusState(Enum):
    EXECUTING = "Выполняется"
    CHECKING = "Проверяется"
    COMPLETED = "Выполнено"
    OVERDUE = "Просрочено"
    DELETED = "Удалено"


@dataclass(frozen=True)
class Status(ValueObject[StatusState]):
    value: StatusState
