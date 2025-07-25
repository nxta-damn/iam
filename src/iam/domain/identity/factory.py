from abc import ABC, abstractmethod

from iam.domain.identity.fullname import Fullname
from iam.domain.identity.user import IdentifiedUser, UserType


class UserFactory(ABC):
    @abstractmethod
    async def create_user(
        self, fullname: Fullname, username: str, password: bytes, user_type: UserType
    ) -> IdentifiedUser: ...
