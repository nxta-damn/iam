from dataclasses import dataclass
from enum import StrEnum

from iam.domain.access.abac.value_objects.policy_attribute import AttributeValue
from iam.domain.access.abac.value_objects.policy_condition import PolicyCondition


class RuleEffect(StrEnum):
    PERMIT = "permit"
    DENY = "deny"


@dataclass(frozen=True, kw_only=True, slots=True)
class PolicyRule:
    name: str
    effect: RuleEffect
    conditions: list[PolicyCondition]

    def __str__(self) -> str:
        return f"Rule {self.name} ({self.effect}): {self.conditions}"

    def __repr__(self) -> str:
        return f"Rule {self.name} ({self.effect}): {self.conditions}"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return all(condition.evaluate(attributes) for condition in self.conditions)
