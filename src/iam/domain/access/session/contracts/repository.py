from abc import ABC, abstractmethod

from iam.domain.access.session.session import IdentifiedAuthSession
from iam.domain.shared.specification import SpecificatedResult, Specification


class AuthSessionRepository(ABC):
    @abstractmethod
    def add(self, session: IdentifiedAuthSession) -> None: ...
    @abstractmethod
    async def delete(self, session: IdentifiedAuthSession) -> None: ...
    @abstractmethod
    async def find(
        self, specification: Specification[IdentifiedAuthSession]
    ) -> SpecificatedResult[IdentifiedAuthSession]: ...
