import requests

from boto3 import client

from src.application.task.interfaces.object_storage import ObjectStorage

from .config import StorageConfig


class YandexStorageService(ObjectStorage):

    def __init__(self, config: StorageConfig) -> None:
        self._config = config

    def _connect_client(self) -> client:
        return client(
            's3',
            aws_access_key_id=self._config.access_key,
            aws_secret_access_key=self._config.secret_key,
            region_name=self._config.region_name,
            endpoint_url=self._config.endpoint_url
        )

    def get(self, name: str) -> bytes:
        s3 = self._connect_client()
        response = s3.get_object(Bucket=self._config.bucket, Key=name)
        return response['Body']

    def upload(self, file: bytes, name: str) -> None:
        s3 = self._connect_client()
        s3.upload_file(file, self._config.bucket, name)


class FirebaseObjectStorage(ObjectStorage):
    def get(self, name: str) -> bytes:
        response = requests.get(name)
        print(response.content)
        if response.status_code == 200:
            return response.content
        return ValueError("Photo can't be download")

    def upload(self, file: bytes, name: str) -> None:
        pass
