from dataclasses import dataclass

import structlog

from iam.domain.identity.repository import UserRepository
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.password_hasher import PasswordHasher

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangePassword(Command[None]):
    old_password: str
    new_password: str


class ChangePasswordHandler(CommandHandler[ChangePassword, None]):
    def __init__(
        self,
        authentication_context: AuthenticationContext,
        password_hasher: PasswordHasher,
        user_repository: UserRepository,
    ) -> None:
        self._authentication_context = authentication_context
        self._password_hasher = password_hasher
        self._user_repository = user_repository

    async def handle(self, command: ChangePassword) -> None:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_user = await self._user_repository.with_user_id(current_user_id)

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        if not self._password_hasher.check_password(command.old_password, current_user.password):
            raise ApplicationError(message="Password is incorrect", error_type=ErrorType.UNAUTHENTICATED)

        current_user.change_password(password=self._password_hasher.hash_password(command.new_password))

        LOGGER.info("Password changed", current_user=current_user_id)
