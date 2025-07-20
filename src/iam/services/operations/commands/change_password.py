from dataclasses import dataclass

import structlog

from iam.domain.identity.contracts.repository import UserRepository
from iam.domain.identity.specifications import IdentifiedUserByIdentitySpec
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.password_hasher import PasswordHasher

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class ChangePassword(Command[None]):
    old_password: str
    new_password: str


class ChangePasswordHandler(CommandHandler[ChangePassword, None]):
    def __init__(
        self,
        event_publisher: EventPublisher,
        authentication_context: AuthenticationContext,
        password_hasher: PasswordHasher,
        user_repository: UserRepository,
    ) -> None:
        self._event_publisher = event_publisher
        self._authentication_context = authentication_context
        self._password_hasher = password_hasher
        self._user_repository = user_repository

    def handle(self, command: ChangePassword) -> None:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        user_by_id_spec = IdentifiedUserByIdentitySpec(identity=current_user_id)
        current_user = self._user_repository.find(user_by_id_spec).first()

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        if not self._password_hasher.check_password(command.old_password, current_user.password):
            raise ApplicationError(message="Password is incorrect", error_type=ErrorType.UNAUTHENTICATED)

        current_user.change_password(password=self._password_hasher.hash_password(command.new_password))

        for event in current_user.raise_events():
            self._event_publisher.publish(event=event)

        LOGGER.info("Password changed", current_user=current_user_id)
