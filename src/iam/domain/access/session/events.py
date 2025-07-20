from dataclasses import dataclass
from datetime import datetime

from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.events import Event
from iam.domain.shared.user_id import UserIdentity


@dataclass(frozen=True, kw_only=True, slots=True)
class SessionCreated(Event):
    identity: SessionIdentity
    user_id: UserIdentity
    expires_at: datetime


@dataclass(frozen=True, kw_only=True, slots=True)
class SessionRevoked(Event):
    identity: SessionIdentity


@dataclass(frozen=True, kw_only=True, slots=True)
class SessionRefreshed(Event):
    identity: SessionIdentity
    expires_at: datetime
