from abc import ABC, abstractmethod

from iam.domain.identity.user import IdentifiedUser, UserType
from iam.domain.identity.value_objects.fullname import Fullname


class UserFactory(ABC):
    @abstractmethod
    async def create_user(
        self, fullname: Fullname, username: str, password: bytes, user_type: UserType = UserType.DEFAULT
    ) -> IdentifiedUser: ...
