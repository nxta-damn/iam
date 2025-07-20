from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import structlog

from iam.domain.access.session.contracts.repository import AuthSessionRepository
from iam.domain.access.session.specifications import IdentifiedSessionByIdentitySpec
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.transaction import Transaction

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshSession(Command[None]): ...


class RefreshSessionHandler(CommandHandler[RefreshSession, None]):
    def __init__(
        self,
        transaction: Transaction,
        event_publisher: EventPublisher,
        auth_session_repository: AuthSessionRepository,
        authentication_context: AuthenticationContext,
    ) -> None:
        self._transaction = transaction
        self._event_publisher = event_publisher
        self._auth_session_repository = auth_session_repository
        self._authentication_context = authentication_context

    def handle(self, _: RefreshSession) -> None:
        current_session_id = self._authentication_context.current_session_id()

        if not current_session_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        session_by_identity_spec = IdentifiedSessionByIdentitySpec(identity=current_session_id)
        current_session = self._auth_session_repository.find(session_by_identity_spec).first()

        if not current_session:
            raise ApplicationError(
                message=f"Session with id: {current_session_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        if current_session.expires_at < datetime.now(UTC):
            raise ApplicationError(
                message=f"Session with id: {current_session_id} is expired", error_type=ErrorType.UNAUTHORIZED
            )

        current_session.prolong_expiration(expires_at=datetime.now(UTC) + timedelta(days=7))

        for event in current_session.raise_events():
            self._event_publisher.publish(event=event)

        self._transaction.commit()

        LOGGER.info("Session refreshed", session_identity=current_session_id)
