from abc import ABC, abstractmethod

from iam.domain.access.abac.abac_policy import IdentifiedPolicy
from iam.domain.shared.specification import SpecificatedResult, Specification


class PolicyRepository(ABC):
    @abstractmethod
    def add(self, policy: IdentifiedPolicy) -> None: ...
    @abstractmethod
    def delete(self, policy: IdentifiedPolicy) -> None: ...
    @abstractmethod
    def find(
        self, specification: Specification[IdentifiedPolicy]
    ) -> SpecificatedResult[IdentifiedPolicy]: ...
