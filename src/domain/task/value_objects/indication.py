from dataclasses import dataclass

from src.domain.common.value_objects import BaseValueObject


@dataclass(frozen=True)
class Indication(BaseValueObject):
    current: float
    previous: float | None
