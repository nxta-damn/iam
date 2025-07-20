import structlog

from iam.domain.access.session.contracts.factory import SessionFactory
from iam.domain.access.session.contracts.repository import AuthSessionRepository
from iam.domain.shared.events import EventHandler
from iam.services.operations.commands.authenticate_user import UserAuthenticated
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.transaction import Transaction

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


class AssignSessionAfterSignInHandler(EventHandler[UserAuthenticated]):
    def __init__(
        self,
        transaction: Transaction,
        session_factory: SessionFactory,
        session_repository: AuthSessionRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self._transaction = transaction
        self._session_factory = session_factory
        self._session_repository = session_repository
        self._event_publisher = event_publisher

    def handle(self, event: UserAuthenticated) -> None:
        session = self._session_factory.authentificate_user(user_id=event.user_id)

        for notification in session.raise_events():
            self._event_publisher.publish(event=notification)

        self._session_repository.add(session=session)
        self._transaction.commit()

        LOGGER.info("Session assigned", user_id=event.user_id, session_id=session.identity)
