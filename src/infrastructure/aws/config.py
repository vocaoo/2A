from dataclasses import dataclass


@dataclass
class StorageConfig:
    access_key: str
    secret_key: str
    endpoint_url: str
    region_name: str
    bucket: str
