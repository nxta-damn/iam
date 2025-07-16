from iam.domain.identity.user import IdentifiedUser
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.specification import Specification
from iam.domain.shared.user_id import UserIdentity


class IdentifiedUserByUsernameSpec(Specification[IdentifiedUser]):
    def __init__(self, username: str) -> None:
        self._username = username

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        if entity:
            return self._username == entity.username
        return False

    @property
    def username(self) -> str:
        return self._username


class IdentifiedUserByIdentitySpec(Specification[IdentifiedUser]):
    def __init__(self, identity: UserIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        if entity:
            return self._identity == entity.identity
        return False

    @property
    def identity(self) -> UserIdentity:
        return self._identity


class IdentifiedUserByFullnameSpec(Specification[IdentifiedUser]):
    def __init__(self, fullname: Fullname) -> None:
        self._fullname = fullname

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        if entity:
            return self._fullname == entity.fullname
        return False

    @property
    def fullname(self) -> Fullname:
        return self._fullname
