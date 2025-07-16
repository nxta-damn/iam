from iam.domain.access.session.session import IdentifiedAuthSession, SessionIdentity
from iam.domain.shared.specification import Specification
from iam.domain.shared.user_id import UserIdentity


class IdentifiedSessionByIdentitySpec(Specification[IdentifiedAuthSession]):
    def __init__(self, identity: SessionIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedAuthSession | None = None) -> bool:
        if entity:
            return self._identity == entity.identity
        return False

    @property
    def identity(self) -> SessionIdentity:
        return self._identity


class IdentifiedSessionByUserIdentitySpec(Specification[IdentifiedAuthSession]):
    def __init__(self, user_id: UserIdentity) -> None:
        self._user_id = user_id

    def is_satisfied_by(self, entity: IdentifiedAuthSession | None = None) -> bool:
        if entity:
            return self._user_id == entity.user_id
        return False

    @property
    def user_id(self) -> UserIdentity:
        return self._user_id
