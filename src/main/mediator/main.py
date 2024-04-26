import logging

from didiator import (
    CommandDispatcherImpl,
    EventObserverImpl,
    Mediator,
    MediatorImpl,
    QueryDispatcherImpl,
)
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiMiddleware, DiScopes
from didiator.middlewares.logging import LoggingMiddleware

from src.application.user.queries.get_user_by_id import GetUserById, GetUserByIdHandler
from src.application.user.queries.get_user_by_username import (
    GetUserByUsername,
    GetUserByUsernameHandler,
)
from src.application.user.queries.get_users import GetUsers, GetUsersHandler
from src.domain.common.events import Event
from src.main.di import DiScope
from src.infrastructure.log.event_handler import EventLogger
from src.application.user.commands import (
    CreateUser,
    CreateUserHandler,
    DeleteUser,
    DeleteUserHandler,
    SetFullName,
    SetFullNameHandler,
    SetUsername,
    SetUsernameHandler,
    SetRole,
    SetRoleHandler,
    SetPassword,
    SetPasswordHandler,
    SetDepartment,
    SetDepartmentHandler,
    SetPhotoURL,
    SetPhotoURLHandler,
    DeleteDepartment,
    DeleteDepartmentHandler,
    DeletePhotoURL,
    DeletePhotoURLHandler,
)
from src.application.task.queries import (
    GetTasks,
    GetTasksHandler,
    GetTaskByCode,
    GetTaskByCodeHandler,
    GetTaskByID,
    GetTaskByIDHandler,
    GetFile,
    GetFileHandler,
)
from src.application.task.commands import (
    CreateTask,
    CreateTaskHandler,
    CheckTask,
    CheckTaskHandler,
    CompleteTask,
    CompleteTaskHandler,
    RejectTask,
    RejectTaskHandler,
    DelayTask,
    DelayTaskHandler,
    DeleteTask,
    DeleteTaskHandler,
    ClearDatabase,
    ClearDatabaseHandler,
    UploadFile,
    UploadFileHandler,
)


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(DiScope.REQUEST)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(CreateUser, CreateUserHandler)
    mediator.register_command_handler(SetUsername, SetUsernameHandler)
    mediator.register_command_handler(SetFullName, SetFullNameHandler)
    mediator.register_command_handler(DeleteUser, DeleteUserHandler)
    mediator.register_command_handler(SetRole, SetRoleHandler)
    mediator.register_command_handler(SetPassword, SetPasswordHandler)
    mediator.register_command_handler(SetDepartment, SetDepartmentHandler)
    mediator.register_command_handler(SetPhotoURL, SetPhotoURLHandler)
    mediator.register_command_handler(DeleteDepartment, DeleteDepartmentHandler)
    mediator.register_command_handler(DeletePhotoURL, DeletePhotoURLHandler)
    mediator.register_command_handler(UploadFile, UploadFileHandler)
    mediator.register_command_handler(ClearDatabase, ClearDatabaseHandler)

    mediator.register_command_handler(CreateTask, CreateTaskHandler)
    mediator.register_command_handler(CheckTask, CheckTaskHandler)
    mediator.register_command_handler(CompleteTask, CompleteTaskHandler)
    mediator.register_command_handler(RejectTask, RejectTaskHandler)
    mediator.register_command_handler(DelayTask, DelayTaskHandler)
    mediator.register_command_handler(DeleteTask, DeleteTaskHandler)

    mediator.register_query_handler(GetUserById, GetUserByIdHandler)
    mediator.register_query_handler(GetUserByUsername, GetUserByUsernameHandler)
    mediator.register_query_handler(GetUsers, GetUsersHandler)
    mediator.register_query_handler(GetFile, GetFileHandler)

    mediator.register_query_handler(GetTaskByID, GetTaskByIDHandler)
    mediator.register_query_handler(GetTaskByCode, GetTaskByCodeHandler)
    mediator.register_query_handler(GetTasks, GetTasksHandler)

    mediator.register_event_handler(Event, EventLogger)
