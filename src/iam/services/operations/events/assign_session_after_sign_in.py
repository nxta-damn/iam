import structlog

from iam.domain.access.factory import SessionFactory
from iam.domain.access.repository import AuthSessionRepository
from iam.domain.shared.events import EventHandler
from iam.services.operations.commands.authenticate_user import UserAuthenticated

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


class AssignSessionAfterSignInHandler(EventHandler[UserAuthenticated]):
    def __init__(self, session_factory: SessionFactory, session_repository: AuthSessionRepository) -> None:
        self._session_factory = session_factory
        self._session_repository = session_repository

    async def handle(self, event: UserAuthenticated) -> None:
        session = await self._session_factory.authentificate_user(user_id=event.user_id)

        self._session_repository.add(session=session)

        LOGGER.info("Session assigned", user_id=event.user_id, session_id=session.identity)
