from iam.domain.access.abac.abac_policy import IdentifiedPolicy
from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget
from iam.domain.shared.specification import Specification


class IdentifiedPolicyByTargetSpec(Specification[IdentifiedPolicy]):
    def __init__(self, target: PolicyTarget) -> None:
        self._target = target

    def is_satisfied_by(self, entity: IdentifiedPolicy | None = None) -> bool:
        return entity.target == self._target if entity else False


class IdentifiedPolicyByIdentitySpec(Specification[IdentifiedPolicy]):
    def __init__(self, identity: PolicyIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedPolicy | None = None) -> bool:
        return entity.identity == self._identity if entity else False
