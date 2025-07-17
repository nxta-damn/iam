from datetime import datetime

from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.events import DomainEventAdder
from iam.domain.shared.user_id import UserIdentity


class IdentifiedAuthSession(IdentifiedEntity[SessionIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: SessionIdentity,
        event_adder: DomainEventAdder,
        *,
        user_id: UserIdentity,
        expires_at: datetime,
    ) -> None:
        IdentifiedEntity.__init__(self, identity)
        EventTrackableEntity.__init__(self, event_adder)

        self._user_id, self._expires_at = user_id, expires_at

    @property
    def user_id(self) -> UserIdentity:
        return self._user_id

    @property
    def expires_at(self) -> datetime:
        return self._expires_at
