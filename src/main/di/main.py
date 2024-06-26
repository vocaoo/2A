from di import Container, bind_by_type
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.application.task.interfaces.object_storage import ObjectStorage
from src.application.user.interfaces.persistence import UserRepo, UserReader
from src.application.common.interfaces.uow import UnitOfWork
from src.application.task.interfaces.persistence import TaskReader, TaskRepo
from src.application.task.interfaces.metadata import PhotoMetadataProcessor
from src.infrastructure.database.main import (
    build_sa_engine,
    build_sa_session,
    build_sa_session_factory,
)
from src.infrastructure.database.repositories.task import TaskReaderImpl, TaskRepoImpl
from src.infrastructure.database.repositories.user import UserRepoImpl, UserReaderImpl
from src.infrastructure.aws import FirebaseObjectStorage
from src.infrastructure.uow import build_uow
from src.infrastructure.metadata import PhotoMetadata
from src.main.di import DiScope
from src.main.mediator import get_mediator
from src.application.task.interfaces.excel import ExcelProcessor
from src.infrastructure.excel.main import OpenpyxlProcessor
from src.application.user.interfaces import IDProvider
from src.infrastructure.auth import JWTIDProvider, JWTProcessor


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DiScope.APP, DiScope.REQUEST]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(Dependent(lambda *args: di_builder, scope=DiScope.APP), DiBuilder)
    )
    di_builder.bind(
        bind_by_type(Dependent(build_uow, scope=DiScope.REQUEST), UnitOfWork)
    )
    setup_mediator_factory(di_builder, get_mediator, DiScope.REQUEST)
    setup_db_factories(di_builder)
    setup_aws_factories(di_builder)
    setup_photo_metadata_factories(di_builder)
    setup_excel_factories(di_builder)
    setup_auth_factories(di_builder)


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator)
    )
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator)
    )
    di_builder.bind(
        bind_by_type(Dependent(mediator_factory, scope=scope), EventMediator)
    )


def setup_db_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(Dependent(build_sa_engine, scope=DiScope.APP), AsyncEngine)
    )
    di_builder.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope=DiScope.APP),
            async_sessionmaker[AsyncSession],
        )
    )
    di_builder.bind(
        bind_by_type(Dependent(build_sa_session, scope=DiScope.REQUEST), AsyncSession)
    )
    di_builder.bind(
        bind_by_type(
            Dependent(TaskRepoImpl, scope=DiScope.REQUEST), TaskRepo, covariant=True
        )
    )
    di_builder.bind(
        bind_by_type(
            Dependent(TaskReaderImpl, scope=DiScope.REQUEST), TaskReader, covariant=True
        )
    )
    di_builder.bind(
        bind_by_type(
            Dependent(UserRepoImpl, scope=DiScope.REQUEST), UserRepo, covariant=True
        )
    )
    di_builder.bind(
        bind_by_type(
            Dependent(UserReaderImpl, scope=DiScope.REQUEST), UserReader, covariant=True
        )
    )


def setup_aws_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(
            Dependent(FirebaseObjectStorage, scope=DiScope.REQUEST), ObjectStorage, covariant=True
        )
    )


def setup_photo_metadata_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(
            Dependent(PhotoMetadata, scope=DiScope.REQUEST), PhotoMetadataProcessor, covariant=True
        )
    )


def setup_excel_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(
            Dependent(OpenpyxlProcessor, scope=DiScope.REQUEST), ExcelProcessor, covariant=True
        )
    )


def setup_auth_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(
        bind_by_type(Dependent(JWTProcessor, scope=DiScope.REQUEST), JWTProcessor)
    )
    di_builder.bind(
        bind_by_type(Dependent(JWTIDProvider, scope=DiScope.REQUEST), IDProvider)
    )
