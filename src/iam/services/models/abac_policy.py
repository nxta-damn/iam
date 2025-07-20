from dataclasses import dataclass

from iam.domain.access.abac.abac_policy import PolicyAlghorithm
from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget


@dataclass(frozen=True, kw_only=True, slots=True)
class AbacPolicyReadModel:
    policy_id: PolicyIdentity
    description: str
    target: PolicyTarget
    rules: list[PolicyRule]
    algorithm: PolicyAlghorithm
