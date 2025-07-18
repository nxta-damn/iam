from datetime import datetime

from iam.domain.access.session.events import SessionRefreshed
from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.user_id import UserIdentity


class IdentifiedAuthSession(IdentifiedEntity[SessionIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: SessionIdentity,
        *,
        user_id: UserIdentity,
        expires_at: datetime,
    ) -> None:
        IdentifiedEntity.__init__(self, identity)

        self.user_id = user_id
        self.expires_at = expires_at

    def prolong_expiration(self, expires_at: datetime) -> None:
        self.expires_at = expires_at
        event = SessionRefreshed(identity=self.identity, expires_at=expires_at)
        self.add_event(event=event)
