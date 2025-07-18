from iam.domain.access.session.session import IdentifiedAuthSession
from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.specification import Specification
from iam.domain.shared.user_id import UserIdentity


class IdentifiedSessionByIdentitySpec(Specification[IdentifiedAuthSession]):
    def __init__(self, identity: SessionIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedAuthSession | None = None) -> bool:
        return self._identity == entity.identity if entity else False


class IdentifiedSessionByUserIdentitySpec(Specification[IdentifiedAuthSession]):
    def __init__(self, user_id: UserIdentity) -> None:
        self._user_id = user_id

    def is_satisfied_by(self, entity: IdentifiedAuthSession | None = None) -> bool:
        return self._user_id == entity.user_id if entity else False
