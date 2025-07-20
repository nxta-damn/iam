from dataclasses import dataclass
from datetime import datetime

from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionReadModel:
    session_id: SessionIdentity
    expires_at: datetime
    assigned_to: UserIdentity
