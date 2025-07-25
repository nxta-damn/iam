import structlog

from iam.domain.access.events import SessionRevoked
from iam.domain.access.repository import AuthSessionRepository
from iam.domain.shared.events import EventHandler
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.operations.commands.unauthenticate_user import UserUnauthenticated
from iam.services.ports.authentication_context import AuthenticationContext

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


class RevokeSessionAfterLogout(EventHandler[UserUnauthenticated]):
    def __init__(
        self, session_repository: AuthSessionRepository, authentication_context: AuthenticationContext
    ) -> None:
        self._session_repository = session_repository
        self._authentication_context = authentication_context

    async def handle(self, event: UserUnauthenticated) -> None:
        current_session_id = self._authentication_context.current_session_id()

        if not current_session_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_session = await self._session_repository.with_session_id(current_session_id)

        if not current_session:
            raise ApplicationError(
                message=f"Session with id {current_session_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        current_session.add_event(event=SessionRevoked(identity=current_session_id))
        await self._session_repository.delete(current_session)

        LOGGER.info("Session revoked", session_id=current_session_id)
