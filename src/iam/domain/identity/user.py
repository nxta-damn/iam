from iam.domain.identity.events import FullnameChanged, PasswordChanged, UsernameChanged
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.events import DomainEventAdder
from iam.domain.shared.user_id import UserIdentity


class IdentifiedUser(IdentifiedEntity[UserIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: UserIdentity,
        event_adder: DomainEventAdder,
        *,
        fullname: Fullname,
        username: str,
        password: bytes,
    ) -> None:
        IdentifiedEntity.__init__(self, identity)
        EventTrackableEntity.__init__(self, event_adder)

        self._fullname = fullname
        self._username = username
        self._password = password

    def change_fullname(self, fullname: Fullname) -> None:
        self._fullname = fullname
        self.add_event(
            event=FullnameChanged(identity=self.identity, fullname=fullname),
        )

    def change_username(self, username: str) -> None:
        self._username = username
        self.add_event(
            event=UsernameChanged(identity=self.identity, username=username),
        )

    def change_password(self, password: bytes) -> None:
        self._password = password
        self.add_event(
            event=PasswordChanged(identity=self.identity, password=password),
        )

    @property
    def fullname(self) -> Fullname:
        return self._fullname

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> bytes:
        return self._password
