from dataclasses import dataclass

from src.domain.common.value_objects.base import ValueObject


@dataclass(frozen=True)
class Comment(ValueObject[str | None]):
    value: str | None
