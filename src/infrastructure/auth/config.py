from dataclasses import dataclass


@dataclass
class JWTConfig:
    secret: str
    algorithm: str
    lifetime_seconds: int
