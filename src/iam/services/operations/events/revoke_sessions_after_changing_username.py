import structlog

from iam.domain.access.session.contracts.repository import AuthSessionRepository
from iam.domain.access.session.events import SessionRevoked
from iam.domain.access.session.specifications import (
    IdentifiedSessionByIdentitySpec,
    IdentifiedSessionByUserIdentitySpec,
)
from iam.domain.identity.events import UsernameChanged
from iam.domain.shared.events import EventHandler
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.transaction import Transaction

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


class RevokeSessionAfterChangingUsername(EventHandler[UsernameChanged]):
    def __init__(
        self,
        transaction: Transaction,
        session_repository: AuthSessionRepository,
        authentication_context: AuthenticationContext,
        event_publisher: EventPublisher,
    ) -> None:
        self._transaction = transaction
        self._session_repository = session_repository
        self._authentication_context = authentication_context
        self._event_publisher = event_publisher

    def handle(self, event: UsernameChanged) -> None:
        current_session_id = self._authentication_context.current_session_id()

        if not current_session_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        session_by_id_spec = IdentifiedSessionByIdentitySpec(current_session_id)
        current_session = self._session_repository.find(session_by_id_spec).first()

        if not current_session:
            raise ApplicationError(
                message=f"Session with id {current_session_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        specification = IdentifiedSessionByUserIdentitySpec(
            event.identity
        ) & ~IdentifiedSessionByIdentitySpec(current_session_id)
        sessions = self._session_repository.find(specification=specification).all()

        for session in sessions:
            self._event_publisher.publish(event=SessionRevoked(identity=session.identity))
            self._session_repository.delete(session=session)

        self._transaction.commit()

        LOGGER.info(
            "Sessions revoked", user_id=event.identity, session_ids=[session.identity for session in sessions]
        )
