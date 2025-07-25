from dataclasses import dataclass

from iam.domain.identity.fullname import Fullname
from iam.domain.shared.user_id import UserIdentity


@dataclass(frozen=True, slots=True, kw_only=True)
class UserReadModel:
    user_id: UserIdentity
    username: str
    fullname: Fullname
