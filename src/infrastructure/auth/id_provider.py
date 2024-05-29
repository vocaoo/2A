from src.application.user.interfaces import IDProvider
from src.domain.user.value_objects import UserID

from .processor import JWTProcessor


class JWTIDProvider(IDProvider):
    def __init__(self, processor: JWTProcessor, token: str) -> None:
        self._processor = processor
        self._token = token

    def get_current_user_id(self) -> UserID:
        return self._processor.decode(self._token)
