from dataclasses import dataclass

from src.domain.common.exceptions import DomainException
from src.domain.common.value_objects import ValueObject


CODE_LENGTH = 15


@dataclass(eq=False)
class WrongCodeValue(DomainException):
    code: str


class IncorrectLengthError(WrongCodeValue):
    @property
    def title(self) -> str:
        return f"The length must be {CODE_LENGTH} characters"


@dataclass(frozen=True)
class Code(ValueObject[str]):
    value: str

    def _validate(self) -> None:
        if len(self.value) != CODE_LENGTH:
            raise IncorrectLengthError(self.value)
