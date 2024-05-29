from datetime import timedelta, datetime, timezone
from typing import Literal
from uuid import UUID

import jwt

from .config import JWTConfig


Algorithm = Literal[
    "HS256", "HS384", "HS512",
    "RS256", "RS384", "RS512",
]


class JWTProcessor:
    def __init__(self, config: JWTConfig) -> None:
        self._config = config

    def generate(self, user_id: UUID) -> str:
        payload = {}
        expire = datetime.now(timezone.utc) + timedelta(seconds=self._config.lifetime_seconds)
        payload.update(exp=expire, user_id=str(user_id))
        return jwt.encode(
            payload=payload,
            key=self._config.secret,
            algorithm=self._config.algorithm,
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(
            jwt=token,
            key=self._config.secret,
            algorithms=[self._config.algorithm],
        )["user_id"]
