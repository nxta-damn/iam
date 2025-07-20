from dataclasses import dataclass
from enum import StrEnum

from iam.domain.access.abac.operators.operators_map import OPERATORS_MAP

type AttributeValue = str | int | list


class AttributeType(StrEnum):
    COLLECTION = "collection"
    STRING = "string"
    NUMERIC = "numeric"


@dataclass(frozen=True, slots=True)
class PolicyAttribute:
    attribute_name: str
    attribute_type: AttributeType
    operator: str
    value: AttributeValue

    def __str__(self) -> str:
        return f"{self.attribute_name}({self.attribute_type}): {self.value}"

    def __repr__(self) -> str:
        return f"PolicyAttribute({self.attribute_name}, {self.attribute_type}, {self.value})"

    def match_attributes(self, attributes: dict[str, AttributeValue]) -> bool:
        attribute_value = attributes.get(self.attribute_name)

        if attribute_value is None:
            return False

        operator_factory = OPERATORS_MAP.get((self.attribute_type, self.operator))
        if not operator_factory:
            return False

        operator = operator_factory(self.value)
        return operator.is_satisfied(attribute_value)
