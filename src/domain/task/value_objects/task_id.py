from dataclasses import dataclass
from uuid import UUID

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class TaskID(ValueObject[UUID]):
    value: UUID
