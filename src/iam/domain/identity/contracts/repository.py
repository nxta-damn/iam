from abc import ABC, abstractmethod

from iam.domain.identity.user import IdentifiedUser
from iam.domain.shared.specification import SpecificatedResult, Specification


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: IdentifiedUser) -> None: ...
    @abstractmethod
    def find(self, specification: Specification[IdentifiedUser]) -> SpecificatedResult[IdentifiedUser]: ...
