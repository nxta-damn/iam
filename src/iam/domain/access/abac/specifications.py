from iam.domain.access.abac.abac_policy import IdentifiedPolicy, PolicyIdentity
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget
from iam.domain.shared.specification import Specification


class IdentifiedPolicyByTargetSpec(Specification[IdentifiedPolicy]):
    def __init__(self, target: PolicyTarget) -> None:
        self._target = target

    def is_satisfied_by(self, entity: IdentifiedPolicy | None = None) -> bool:
        if entity:
            return entity.target == self._target
        return False

    @property
    def target(self) -> PolicyTarget:
        return self._target


class IdentifiedPolicyByIdentitySpec(Specification[IdentifiedPolicy]):
    def __init__(self, identity: PolicyIdentity) -> None:
        self._identity = identity

    def is_satisfied_by(self, entity: IdentifiedPolicy | None = None) -> bool:
        if entity:
            return entity.identity == self._identity
        return False

    @property
    def identity(self) -> PolicyIdentity:
        return self._identity
