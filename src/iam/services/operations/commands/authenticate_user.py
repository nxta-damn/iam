from dataclasses import dataclass

import structlog

from iam.domain.identity.repository import UserRepository
from iam.domain.shared.events import Event
from iam.domain.shared.user_id import UserIdentity
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.password_hasher import PasswordHasher

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthenticateUser(Command[UserIdentity]):
    username: str
    raw_password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class UserAuthenticated(Event):
    user_id: UserIdentity


class AuthenticateUserHandler(CommandHandler[AuthenticateUser, UserIdentity]):
    def __init__(
        self,
        authentication_context: AuthenticationContext,
        password_hasher: PasswordHasher,
        user_repository: UserRepository,
    ) -> None:
        self._authentication_context = authentication_context
        self._password_hasher = password_hasher
        self._user_repository = user_repository

    async def handle(self, command: AuthenticateUser) -> UserIdentity:
        current_user_id = self._authentication_context.current_user_id()

        if current_user_id:
            raise ApplicationError(
                message="User is already authenticated", error_type=ErrorType.UNAUTHENTICATED
            )

        existing_user = await self._user_repository.with_username(command.username)

        if not existing_user:
            raise ApplicationError(
                message=f"User with username: {command.username} is not found", error_type=ErrorType.NOT_FOUND
            )

        if not self._password_hasher.check_password(command.raw_password, existing_user.password):
            raise ApplicationError(message="Password is incorrect", error_type=ErrorType.UNAUTHENTICATED)

        existing_user.add_event(event=UserAuthenticated(user_id=existing_user.identity))

        LOGGER.info("User signed in", username=command.username)

        return existing_user.identity
