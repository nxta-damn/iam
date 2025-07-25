from enum import StrEnum

from iam.domain.identity.events import FullnameChanged, PasswordChanged, UsernameChanged
from iam.domain.identity.fullname import Fullname
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.events import EventTracker
from iam.domain.shared.user_id import UserIdentity


class UserType(StrEnum):
    DEFAULT = "default-user"
    SUPER_USER = "super-user"


class IdentifiedUser(IdentifiedEntity[UserIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: UserIdentity,
        event_tracker: EventTracker,
        *,
        fullname: Fullname,
        username: str,
        password: bytes,
        user_type: UserType = UserType.DEFAULT,
    ) -> None:
        IdentifiedEntity.__init__(self, identity=identity)
        EventTrackableEntity.__init__(self, event_tracker=event_tracker)

        self.fullname = fullname
        self.username = username
        self.password = password
        self.user_type = user_type

    def change_fullname(self, fullname: Fullname) -> None:
        self.fullname = fullname
        event = FullnameChanged(identity=self.identity, fullname=fullname)
        self.add_event(event=event)

    def change_username(self, username: str) -> None:
        self.username = username
        event = UsernameChanged(identity=self.identity, username=username)
        self.add_event(event=event)

    def change_password(self, password: bytes) -> None:
        self.password = password
        event = PasswordChanged(identity=self.identity, password=password)
        self.add_event(event=event)
