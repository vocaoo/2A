from dataclasses import dataclass

from src.domain.common.value_objects import BaseValueObject


@dataclass(frozen=True)
class Coordinates(BaseValueObject):
    latitude: float | None
    longitude: float | None
