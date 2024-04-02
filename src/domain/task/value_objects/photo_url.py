from dataclasses import dataclass

from src.domain.common.value_objects import BaseValueObject


@dataclass(frozen=True)
class PhotoURL(BaseValueObject):
    near: str | None
    far: str | None
