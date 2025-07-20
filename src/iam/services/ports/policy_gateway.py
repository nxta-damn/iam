from abc import ABC, abstractmethod

from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.services.models.abac_policy import AbacPolicyReadModel
from iam.services.models.pagination import Pagination


class AbacPolicyGateway(ABC):
    @abstractmethod
    def with_id(self, policy_id: PolicyIdentity) -> AbacPolicyReadModel | None: ...
    @abstractmethod
    def load_many(self, pagination: Pagination) -> list[AbacPolicyReadModel]: ...
