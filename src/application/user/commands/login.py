import logging
from dataclasses import dataclass
from uuid import UUID

from didiator import EventMediator

from src.application.common.command import Command, CommandHandler
from src.application.common.interfaces.uow import UnitOfWork
from src.application.user.interfaces.persistence import UserRepo
from src.domain.user.value_objects import Username, Password
from src.infrastructure.auth import JWTProcessor


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoginCommand(Command[UUID]):
    username: str
    password: str


class LoginHandler(CommandHandler[LoginCommand, UUID]):
    def __init__(
        self,
        user_repo: UserRepo,
        uow: UnitOfWork,
        mediator: EventMediator,
        processor: JWTProcessor,
    ) -> None:
        self._user_repo = user_repo
        self._uow = uow
        self._mediator = mediator
        self._processor = processor

    async def __call__(self, command: LoginCommand) -> UUID:
        username = Username(command.username)
        password = Password(command.password)

        user = await self._user_repo.acquire_user_by_username(username)
        user.check_password(password)

        user_id = user.user_id.to_raw()
        print(user_id)
        token = self._processor.generate(user_id)

        logger.info(f"User with {user_id} is login")

        return token
