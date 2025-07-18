from iam.domain.identity.events import FullnameChanged, PasswordChanged, UsernameChanged
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.user_id import UserIdentity


class IdentifiedUser(IdentifiedEntity[UserIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: UserIdentity,
        *,
        fullname: Fullname,
        username: str,
        password: bytes,
    ) -> None:
        IdentifiedEntity.__init__(self, identity)

        self.fullname = fullname
        self.username = username
        self.password = password

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
