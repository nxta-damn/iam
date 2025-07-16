from dataclasses import dataclass

from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.events import DomainEvent
from iam.domain.shared.user_id import UserIdentity


@dataclass(frozen=True, kw_only=True, slots=True)
class UserCreated(DomainEvent):
    identity: UserIdentity
    username: str
    fullname: Fullname
    password: bytes


@dataclass(frozen=True, kw_only=True, slots=True)
class FullnameChanged(DomainEvent):
    identity: UserIdentity
    fullname: Fullname


@dataclass(frozen=True, kw_only=True, slots=True)
class UsernameChanged(DomainEvent):
    identity: UserIdentity
    username: str


@dataclass(frozen=True, kw_only=True, slots=True)
class PasswordChanged(DomainEvent):
    identity: UserIdentity
    password: bytes
