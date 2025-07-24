from datetime import UTC, datetime, timedelta
from typing import Final, cast
from uuid import uuid4

from iam.adapters.persistence.uow_tracker import UoWTracker
from iam.adapters.session_proxy import SessionProxy
from iam.domain.access.session.contracts.factory import SessionFactory
from iam.domain.access.session.events import SessionCreated
from iam.domain.access.session.session import IdentifiedAuthSession
from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity


class SessionFactoryImpl(SessionFactory):
    _SESSION_LIFETIME: Final = datetime.now(UTC) + timedelta(days=15)

    def __init__(self, uow_tracker: UoWTracker) -> None:
        self._uow_tracker = uow_tracker

    async def authentificate_user(self, user_id: UserIdentity) -> IdentifiedAuthSession:
        session = IdentifiedAuthSession(
            identity=SessionIdentity(uuid4()), user_id=user_id, expires_at=self._SESSION_LIFETIME
        )
        event = SessionCreated(
            identity=session.identity, user_id=session.user_id, expires_at=session.expires_at
        )
        session_proxy = SessionProxy(session=session, uow_tracker=self._uow_tracker)

        session.add_event(event=event)
        return cast("IdentifiedAuthSession", session_proxy)
