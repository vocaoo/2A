from abc import abstractmethod
from typing import Protocol

from src.domain.task.value_objects import Coordinates


class PhotoMetadataProcessor(Protocol):
    @abstractmethod
    def get_coordinates(self, photo: bytes) -> Coordinates:
        raise NotImplementedError
