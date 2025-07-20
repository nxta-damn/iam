from dataclasses import dataclass

from iam.domain.access.abac.value_objects.policy_attribute import AttributeValue, PolicyAttribute


@dataclass(frozen=True, slots=True, kw_only=True)
class Subject:
    attributes: list[PolicyAttribute]

    def __str__(self) -> str:
        return ", ".join(str(attr) for attr in self.attributes)

    def __repr__(self) -> str:
        return f"Subject({self.attributes})"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return all(attr.match_attributes(attributes) for attr in self.attributes)


@dataclass(frozen=True, slots=True, kw_only=True)
class Resource:
    attributes: list[PolicyAttribute]

    def __str__(self) -> str:
        return ", ".join(str(attr) for attr in self.attributes)

    def __repr__(self) -> str:
        return f"Resource({self.attributes})"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return all(attr.match_attributes(attributes) for attr in self.attributes)


@dataclass(frozen=True, slots=True, kw_only=True)
class Environment:
    attributes: list[PolicyAttribute]

    def __str__(self) -> str:
        return ", ".join(str(attr) for attr in self.attributes)

    def __repr__(self) -> str:
        return f"Environment({self.attributes})"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return all(attr.match_attributes(attributes) for attr in self.attributes)


@dataclass(frozen=True, slots=True, kw_only=True)
class Action:
    attributes: list[PolicyAttribute]

    def __str__(self) -> str:
        return ", ".join(str(attr) for attr in self.attributes)

    def __repr__(self) -> str:
        return f"Action({self.attributes})"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return all(attr.match_attributes(attributes) for attr in self.attributes)


@dataclass(frozen=True, slots=True, kw_only=True)
class PolicyCondition:
    subject: Subject
    resource: Resource
    action: Action
    environment: Environment

    def __str__(self) -> str:
        return f"Subject: {self.subject}\nResource: {self.resource}\nAction: {self.action}"

    def __repr__(self) -> str:
        return f"PolicyContext({self.subject}, {self.resource}, {self.action})"

    def evaluate(self, attributes: dict[str, AttributeValue]) -> bool:
        return (
            self.subject.evaluate(attributes=attributes)
            and self.action.evaluate(attributes=attributes)
            and self.resource.evaluate(attributes=attributes)
            and self.environment.evaluate(attributes=attributes)
        )
