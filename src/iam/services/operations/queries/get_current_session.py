from dataclasses import dataclass
from datetime import UTC, datetime

from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Query, QueryHandler
from iam.services.models.session import SessionReadModel
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.session_gateway import SessionGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentSession(Query[SessionReadModel]): ...


class GetCurrentSessionHandler(QueryHandler[GetCurrentSession, SessionReadModel]):
    def __init__(
        self,
        session_gateway: SessionGateway,
        authentication_context: AuthenticationContext,
    ) -> None:
        self._session_gateway = session_gateway
        self._authentication_context = authentication_context

    def handle(self, query: GetCurrentSession) -> SessionReadModel:
        current_session_id = self._authentication_context.current_session_id()

        if not current_session_id:
            raise ApplicationError(
                message="Session is not authenticated", error_type=ErrorType.UNAUTHENTICATED
            )

        current_session = self._session_gateway.with_id(session_id=current_session_id)

        if not current_session:
            raise ApplicationError(
                message=f"Session with id: {current_session_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        if current_session.expires_at < datetime.now(UTC):
            raise ApplicationError(
                message=f"Session with id: {current_session_id} expired", error_type=ErrorType.UNAUTHENTICATED
            )

        return current_session
