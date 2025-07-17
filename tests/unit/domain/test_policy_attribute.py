from pytest import mark

from iam.domain.access.abac.value_objects.policy_attribute import AttributeType, PolicyAttribute


@mark.parametrize(
    'attribute, attributes', [
        (PolicyAttribute("role", AttributeType.STRING, "eq", "admin"), {"role": "admin"})
    ]
)
def test_policy_attribute_should_match_when_string_equals(
    attribute: PolicyAttribute, attributes: dict[str, str]
) -> None:
    result = attribute.match_attributes(attributes)

    assert result is True


@mark.parametrize(
    'attribute, attributes', [
        (PolicyAttribute("role", AttributeType.STRING, "eq", "admin"), {"role": "user"})
    ]
)
def test_policy_attribute_should_not_match_when_string_not_equals(
    attribute: PolicyAttribute, attributes: dict[str, str]
) -> None:
    result = attribute.match_attributes(attributes)

    assert result is False


@mark.parametrize(
    'attribute, attributes', [
        (PolicyAttribute("role", AttributeType.STRING, "not_eq", "admin"), {"role": "user"})
    ]
)
def test_policy_attribute_should_match_when_string_not_equal_operator(
    attribute: PolicyAttribute, attributes: dict[str, str]
) -> None:
    result = attribute.match_attributes(attributes)

    assert result is True


@mark.parametrize(
    'attribute, attributes', [
        (PolicyAttribute("age", AttributeType.NUMERIC, "gt", 18), {"age": 21})
    ]
)
def test_policy_attribute_should_match_when_numeric_greater_than(
    attribute: PolicyAttribute, attributes: dict[str, int]
) -> None:
    result = attribute.match_attributes(attributes)

    assert result is True


@mark.parametrize(
    'attribute, attributes', [
        (PolicyAttribute("groups", AttributeType.COLLECTION, "in", ["admin", "user"]), {"groups": "admin"})
    ]
)
def test_policy_attribute_should_match_when_collection_in(
    attribute: PolicyAttribute, attributes: dict[str, str]
) -> None:
    result = attribute.match_attributes(attributes)

    assert result is True
