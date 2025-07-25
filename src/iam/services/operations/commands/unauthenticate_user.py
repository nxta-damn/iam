from dataclasses import dataclass

import structlog

from iam.domain.identity.repository import UserRepository
from iam.domain.shared.events import Event
from iam.domain.shared.user_id import UserIdentity
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class UnauthenticateUser(Command[None]): ...


@dataclass(frozen=True, slots=True, kw_only=True)
class UserUnauthenticated(Event):
    user_id: UserIdentity


class UnauthenticateUserHandler(CommandHandler[UnauthenticateUser, None]):
    def __init__(
        self, authentication_context: AuthenticationContext, user_repository: UserRepository
    ) -> None:
        self._authentication_context = authentication_context
        self._user_repository = user_repository

    async def handle(self, command: UnauthenticateUser) -> None:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_user = await self._user_repository.with_user_id(current_user_id)

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        current_user.add_event(event=UserUnauthenticated(user_id=current_user_id))

        LOGGER.info("User logged out", current_user=current_user_id)
