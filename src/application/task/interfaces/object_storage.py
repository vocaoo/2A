from typing import Protocol


class ObjectStorage(Protocol):
    def get(self, name: str) -> bytes:
        raise NotImplementedError

    def upload(self, file: bytes, name: str) -> None:
        raise NotImplementedError
