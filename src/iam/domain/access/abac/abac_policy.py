from enum import StrEnum

from iam.domain.access.abac.events import PolicyAlghorithmChanged, PolicyDescriptionChanged
from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.value_objects.policy_attribute import AttributeValue
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule, RuleEffect
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity


class PolicyAlghorithm(StrEnum):
    ALLOW_OVERRIDES = "allow_overrides"
    DENY_OVERRIDES = "deny_overrides"


class IdentifiedPolicy(IdentifiedEntity[PolicyIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: PolicyIdentity,
        *,
        description: str,
        target: PolicyTarget,
        rules: list[PolicyRule],
        alghorithm: PolicyAlghorithm = PolicyAlghorithm.ALLOW_OVERRIDES,
    ) -> None:
        IdentifiedEntity.__init__(self, identity=identity)

        self.description = description
        self.alghorithm = alghorithm
        self.rules = rules
        self.target = target

    def change_description(self, description: str) -> None:
        self.description = description
        event = PolicyDescriptionChanged(identity=self.identity, description=self.description)
        self.add_event(event=event)

    def change_alghorithm(self, alghorithm: PolicyAlghorithm) -> None:
        self.alghorithm = alghorithm
        event = PolicyAlghorithmChanged(identity=self.identity, alghorithm=self.alghorithm)
        self.add_event(event=event)

    def is_allowed(self, attributes: dict[str, AttributeValue]) -> bool:
        matching_rules = [rule for rule in self.rules if rule.evaluate(attributes=attributes)]

        if self.alghorithm == PolicyAlghorithm.DENY_OVERRIDES and matching_rules:
            return all(rule.effect == RuleEffect.PERMIT for rule in matching_rules)

        if self.alghorithm == PolicyAlghorithm.ALLOW_OVERRIDES and matching_rules:
            return any(rule.effect == RuleEffect.PERMIT for rule in matching_rules)

        return False
