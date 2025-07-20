from dataclasses import dataclass, field

from iam.domain.identity.user import UserType
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.events import Event
from iam.domain.shared.user_id import UserIdentity


@dataclass(frozen=True, kw_only=True, slots=True)
class UserCreated(Event):
    identity: UserIdentity
    username: str
    fullname: Fullname
    password: bytes
    user_type: UserType = field(default=UserType.DEFAULT)


@dataclass(frozen=True, kw_only=True, slots=True)
class FullnameChanged(Event):
    identity: UserIdentity
    fullname: Fullname


@dataclass(frozen=True, kw_only=True, slots=True)
class UsernameChanged(Event):
    identity: UserIdentity
    username: str


@dataclass(frozen=True, kw_only=True, slots=True)
class PasswordChanged(Event):
    identity: UserIdentity
    password: bytes
