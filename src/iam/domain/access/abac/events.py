from dataclasses import dataclass

from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule
from iam.domain.shared.events import DomainEvent


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyCreated(DomainEvent):
    identity: PolicyIdentity
    description: str
    alghorithm: str
    rules: list[PolicyRule]


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyAlghorithmChanged(DomainEvent):
    identity: PolicyIdentity
    alghorithm: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyDescriptionChanged(DomainEvent):
    identity: PolicyIdentity
    description: str


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyRemoved(DomainEvent):
    identity: PolicyIdentity
