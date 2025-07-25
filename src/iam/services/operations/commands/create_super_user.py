from dataclasses import dataclass

import structlog

from iam.domain.identity.factory import UserFactory
from iam.domain.identity.fullname import Fullname
from iam.domain.identity.repository import UserRepository
from iam.domain.identity.user import UserType
from iam.domain.shared.user_id import UserIdentity
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.password_hasher import PasswordHasher

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, kw_only=True, slots=True)
class CreateSuperUser(Command[UserIdentity]):
    fullaname: Fullname
    username: str
    raw_password: str


class CreateSuperUserHandler(CommandHandler[CreateSuperUser, UserIdentity]):
    def __init__(
        self,
        password_hasher: PasswordHasher,
        user_factory: UserFactory,
        user_repository: UserRepository,
    ) -> None:
        self._password_hasher = password_hasher
        self._user_factory = user_factory
        self._user_repository = user_repository

    async def handle(self, command: CreateSuperUser) -> UserIdentity:
        existing_user = await self._user_repository.with_username(command.username)

        if existing_user:
            raise ApplicationError(
                message=f"User with username {command.username} exists",
                error_type=ErrorType.CONFLICT,
            )

        super_user = await self._user_factory.create_user(
            fullname=command.fullaname,
            username=command.username,
            password=self._password_hasher.hash_password(command.raw_password),
            user_type=UserType.SUPER_USER,
        )

        self._user_repository.add(super_user)

        LOGGER.info("Super user created", username=command.username, fullname=command.fullaname)

        return super_user.identity
