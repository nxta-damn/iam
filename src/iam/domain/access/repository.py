from abc import ABC, abstractmethod

from iam.domain.access.session import IdentifiedAuthSession
from iam.domain.access.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity


class AuthSessionRepository(ABC):
    @abstractmethod
    def add(self, session: IdentifiedAuthSession) -> None: ...
    @abstractmethod
    async def delete(self, session: IdentifiedAuthSession) -> None: ...
    @abstractmethod
    async def with_session_id(self, session_id: SessionIdentity) -> IdentifiedAuthSession | None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserIdentity) -> list[IdentifiedAuthSession]: ...
