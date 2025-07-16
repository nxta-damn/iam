from enum import StrEnum

from iam.domain.access.abac.abac_policy import PolicyAlghorithm
from iam.domain.access.abac.contracts.policy_repository import PolicyRepository
from iam.domain.access.abac.specifications import IdentifiedPolicyByTargetSpec
from iam.domain.access.abac.value_objects.policy_attribute import AttributeValue
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget


class Decision(StrEnum):
    ALLOW = "allow"
    DENY = "deny"


class AccessEvaluator:
    def __init__(self, policy_repository: PolicyRepository) -> None:
        self._policy_repository = policy_repository

    def evaluate(self, traget: PolicyTarget, attributes: dict[str, AttributeValue]) -> Decision:
        policies = self._policy_repository.find(IdentifiedPolicyByTargetSpec(target=traget)).all()

        for abac_policy in policies:
            is_allowed = abac_policy.is_allowed(attributes=attributes)
            if is_allowed and abac_policy.alghorithm == PolicyAlghorithm.ALLOW_OVERRIDES:
                return Decision.ALLOW
            if not is_allowed and abac_policy.alghorithm == PolicyAlghorithm.DENY_OVERRIDES:
                return Decision.DENY

        return Decision.DENY
