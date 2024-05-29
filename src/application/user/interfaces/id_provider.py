from abc import abstractmethod
from typing import Protocol

from src.domain.user.value_objects import UserID


class IDProvider(Protocol):
    @abstractmethod
    def get_current_user_id(self) -> UserID:
        raise NotImplementedError
