from datetime import datetime

from iam.adapters.persistence.uow_tracker import UoWTracker
from iam.domain.access.session.session import IdentifiedAuthSession
from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity


class SessionProxy:
    def __init__(self, session: IdentifiedAuthSession, uow_tracker: UoWTracker) -> None:
        self.session = session
        self.uow_tracker = uow_tracker

    def prolong_expiration(self, expires_at: datetime) -> None:
        self.session.prolong_expiration(expires_at=expires_at)
        self.uow_tracker.register_dirty(model=self.session)

    @property
    def identity(self) -> SessionIdentity:
        return self.session.identity

    @property
    def user_id(self) -> UserIdentity:
        return self.session.user_id

    @property
    def expires_at(self) -> datetime:
        return self.session.expires_at
