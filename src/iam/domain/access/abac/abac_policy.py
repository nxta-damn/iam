from enum import StrEnum
from typing import NewType

from iam.domain.access.abac.events import PolicyAlghorithmChanged, PolicyDescriptionChanged
from iam.domain.access.abac.value_objects.policy_attribute import AttributeValue
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule, RuleEffect
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget
from iam.domain.shared.entity import EventTrackableEntity, IdentifiedEntity
from iam.domain.shared.events import DomainEventAdder

PolicyIdentity = NewType("PolicyIdentity", str)


class PolicyAlghorithm(StrEnum):
    ALLOW_OVERRIDES = "allow_overrides"
    DENY_OVERRIDES = "deny_overrides"


class IdentifiedPolicy(IdentifiedEntity[PolicyIdentity], EventTrackableEntity):
    def __init__(
        self,
        identity: PolicyIdentity,
        event_adder: DomainEventAdder,
        *,
        description: str,
        target: PolicyTarget,
        rules: list[PolicyRule],
        alghorithm: PolicyAlghorithm = PolicyAlghorithm.ALLOW_OVERRIDES,
    ) -> None:
        EventTrackableEntity.__init__(self, event_adder=event_adder)
        IdentifiedEntity.__init__(self, identity=identity)

        self._description = description
        self._alghorithm = alghorithm
        self._rules = rules
        self._target = target

    def change_description(self, description: str) -> None:
        self._description = description
        event = PolicyDescriptionChanged(identity=self._identity, description=self._description)
        self.add_event(event=event)

    def change_alghorithm(self, alghorithm: PolicyAlghorithm) -> None:
        self._alghorithm = alghorithm
        event = PolicyAlghorithmChanged(identity=self._identity, alghorithm=self._alghorithm)
        self.add_event(event=event)

    def is_allowed(self, attributes: dict[str, AttributeValue]) -> bool:
        for rule in self.rules:
            if rule.evaluate(attributes=attributes):
                return rule.effect == RuleEffect.PERMIT

        return False

    @property
    def target(self) -> PolicyTarget:
        return self._target

    @property
    def alghorithm(self) -> PolicyAlghorithm:
        return self._alghorithm

    @property
    def rules(self) -> list[PolicyRule]:
        return self._rules.copy()

    @property
    def description(self) -> str:
        return self._description
