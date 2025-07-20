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
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.password_hasher import PasswordHasher
from iam.services.ports.transaction import Transaction

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
        event_publisher: EventPublisher,
        user_factory: UserFactory,
        user_repository: UserRepository,
        transaction: Transaction,
    ) -> None:
        self._password_hasher = password_hasher
        self._event_publisher = event_publisher
        self._user_factory = user_factory
        self._user_repository = user_repository
        self._transacction = transaction

    def handle(self, command: CreateSuperUser) -> UserIdentity:
        specification = IdentifiedUserByUsernameSpec(username=command.username)
        existing_user = self._user_repository.find(specification=specification).first()

        if existing_user:
            raise ApplicationError(
                message=f"User with username {command.username} already exists",
                error_type=ErrorType.CONFLICT,
            )

        super_user = self._user_factory.create_user(
            fullname=command.fullaname,
            username=command.username,
            password=self._password_hasher.hash_password(command.raw_password),
            user_type=UserType.SUPER_USER,
        )

        for event in super_user.raise_events():
            self._event_publisher.publish(event=event)

        self._user_repository.add(super_user)
        self._transacction.commit()

        LOGGER.info("Super user created", username=command.username, fullname=command.fullaname)

        return super_user.identity
