from dataclasses import dataclass

import structlog

from iam.domain.identity.factory import UserFactory
from iam.domain.identity.fullname import Fullname
from iam.domain.identity.repository import UserRepository
from iam.domain.identity.user import UserType
from iam.domain.shared.user_id import UserIdentity
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.password_hasher import PasswordHasher
from iam.services.ports.transaction import Transaction

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterUserViaBasic(Command[UserIdentity]):
    fullname: Fullname
    username: str
    raw_password: str


class RegisterUserHandler(CommandHandler[RegisterUserViaBasic, UserIdentity]):
    def __init__(
        self,
        transaction: Transaction,
        user_factory: UserFactory,
        user_repository: UserRepository,
        authentication_context: AuthenticationContext,
        password_hasher: PasswordHasher,
    ) -> None:
        self._transaction = transaction
        self._user_factory = user_factory
        self._user_repository = user_repository
        self._authentication_context = authentication_context
        self._password_hasher = password_hasher

    async def handle(self, command: RegisterUserViaBasic) -> UserIdentity:
        current_user_id = self._authentication_context.current_user_id()

        if current_user_id:
            raise ApplicationError(
                message="User is already authenticated", error_type=ErrorType.UNAUTHENTICATED
            )

        existing_user = await self._user_repository.with_username(command.username)

        if existing_user:
            raise ApplicationError(
                message=f"User with username: {command.username} exists", error_type=ErrorType.CONFLICT
            )

        user = await self._user_factory.create_user(
            fullname=command.fullname,
            username=command.username,
            user_type=UserType.DEFAULT,
            password=self._password_hasher.hash_password(command.raw_password),
        )

        self._user_repository.add(user)
        await self._transaction.flush()

        LOGGER.info("User signed up", username=command.username, fullname=command.fullname)

        return user.identity
