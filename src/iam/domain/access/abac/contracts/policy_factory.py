from abc import ABC, abstractmethod

from iam.domain.access.abac.abac_policy import IdentifiedPolicy, PolicyAlghorithm
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget


class IdentififedPolicyFactory(ABC):
    @abstractmethod
    def create(
        self,
        description: str,
        target: PolicyTarget,
        rules: list[PolicyRule],
        algorithm: PolicyAlghorithm,
    ) -> IdentifiedPolicy: ...
