import structlog

from iam.domain.access.factory import SessionFactory
from iam.domain.access.repository import AuthSessionRepository
from iam.domain.identity.events import UserCreated
from iam.domain.identity.user import UserType
from iam.domain.shared.events import EventHandler

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


class AssignSessionAfterSignInHandler(EventHandler[UserCreated]):
    def __init__(self, session_factory: SessionFactory, session_repository: AuthSessionRepository) -> None:
        self._session_factory = session_factory
        self._session_repository = session_repository

    async def handle(self, event: UserCreated) -> None:
        if event.user_type == UserType.SUPER_USER:
            return

        session = await self._session_factory.authentificate_user(user_id=event.identity)

        self._session_repository.add(session=session)

        LOGGER.info("Session assigned", user_id=event.identity, session_id=session.identity)
