from dataclasses import dataclass, field

from di import bind_by_type
from di.dependent import Dependent
from didiator.interface.utils.di_builder import DiBuilder

from src.infrastructure.database.config import DBConfig
from src.main.di import DiScope
from src.infrastructure.log import LoggingConfig
from src.infrastructure.aws.config import StorageConfig


@dataclass
class APIConfig:
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = __debug__


@dataclass
class Config:
    db: DBConfig = field(default_factory=DBConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    api: APIConfig = field(default_factory=APIConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DBConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.logging, scope=DiScope.APP), LoggingConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.api, scope=DiScope.APP), APIConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.storage, scope=DiScope.APP), StorageConfig))
