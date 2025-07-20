from dataclasses import dataclass

import structlog

from iam.domain.identity.contracts.factory import UserFactory
from iam.domain.identity.contracts.repository import UserRepository
from iam.domain.identity.specifications import IdentifiedUserByUsernameSpec
from iam.domain.identity.user import UserType
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.user_id import UserIdentity
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.event_publisher import EventPublisher
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
        event_publisher: EventPublisher,
        authentication_context: AuthenticationContext,
        password_hasher: PasswordHasher,
    ) -> None:
        self._transaction = transaction
        self._user_factory = user_factory
        self._user_repository = user_repository
        self._event_publisher = event_publisher
        self._authentication_context = authentication_context
        self._password_hasher = password_hasher

    def handle(self, command: RegisterUserViaBasic) -> UserIdentity:
        current_user_id = self._authentication_context.current_user_id()

        if current_user_id:
            raise ApplicationError(
                message="User is already authenticated", error_type=ErrorType.UNAUTHENTICATED
            )

        user_by_username_spec = IdentifiedUserByUsernameSpec(username=command.username)
        existing_user = self._user_repository.find(user_by_username_spec).first()

        if existing_user:
            raise ApplicationError(
                message=f"User with username: {command.username} exists", error_type=ErrorType.CONFLICT
            )

        user = self._user_factory.create_user(
            fullname=command.fullname,
            username=command.username,
            user_type=UserType.DEFAULT,
            password=self._password_hasher.hash_password(command.raw_password),
        )

        for event in user.raise_events():
            self._event_publisher.publish(event=event)

        self._user_repository.add(user)
        self._transaction.flush()

        LOGGER.info("User signed up", username=command.username, fullname=command.fullname)

        return user.identity
