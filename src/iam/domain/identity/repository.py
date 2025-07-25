from abc import ABC, abstractmethod

from iam.domain.identity.user import IdentifiedUser
from iam.domain.shared.user_id import UserIdentity


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: IdentifiedUser) -> None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserIdentity) -> IdentifiedUser | None: ...
    @abstractmethod
    async def with_username(self, username: str) -> IdentifiedUser | None: ...
