from iam.domain.identity.user import IdentifiedUser
from iam.domain.identity.value_objects.fullname import Fullname
from iam.domain.shared.specification import Specification
from iam.domain.shared.user_id import UserIdentity


class IdentifiedUserByUsernameSpec(Specification[IdentifiedUser]):
    def __init__(self, username: str) -> None:
        self._username = username

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        return self._username == entity.username if entity else False


class IdentifiedUserByIdentitySpec(Specification[IdentifiedUser]):
    def __init__(self, identity: UserIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        return self._identity == entity.identity if entity else False


class IdentifiedUserByFullnameSpec(Specification[IdentifiedUser]):
    def __init__(self, fullname: Fullname) -> None:
        self._fullname = fullname

    def is_satisfied_by(self, entity: IdentifiedUser | None = None) -> bool:
        return self._fullname == entity.fullname if entity else False
