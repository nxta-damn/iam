from unittest.mock import create_autospec

from pytest import fixture

from iam.domain.access.abac.abac_policy import IdentifiedPolicy
from iam.domain.access.abac.contracts.policy_repository import PolicyRepository
from iam.domain.access.abac.services.access_evaluator import AccessEvaluator, Decision
from iam.domain.access.abac.value_objects.policy_target import PolicyTarget
from iam.domain.shared.specification import SpecificatedResult


@fixture(scope='function')
def specificated_result() -> SpecificatedResult:
    mocked_specificated_result = create_autospec(SpecificatedResult)
    return mocked_specificated_result


@fixture(scope='function')
def policy_repository(specificated_result: SpecificatedResult) -> PolicyRepository:
    mocked_policy_repository = create_autospec(PolicyRepository)
    mocked_policy_repository.find.return_value = specificated_result
    return mocked_policy_repository


@fixture(scope='function')
def access_evaluator(policy_repository: PolicyRepository) -> AccessEvaluator:
    return AccessEvaluator(policy_repository=policy_repository)


def test_default_deny_when_no_policies_found(
    access_evaluator: AccessEvaluator
) -> None:
    # Arrange
    target = PolicyTarget(subjects=[], resources=[], actions=[], environments=[])
    attrs = {'role': 'admin'}
    access_evaluator._policy_repository.find.return_value.all.return_value = []

    # Act
    decision = access_evaluator.evaluate(traget=target, attributes=attrs)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.DENY


def test_allow_when_allow_overrides_policy_permits_access(
    access_evaluator: AccessEvaluator, admin_allow_policy: IdentifiedPolicy,
    standard_target: PolicyTarget, standard_attributes: dict[str, str]
) -> None:
    # Arrange
    access_evaluator._policy_repository.find.return_value.all.return_value = [admin_allow_policy]

    # Act
    decision = access_evaluator.evaluate(traget=standard_target, attributes=standard_attributes)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.ALLOW


def test_deny_when_deny_overrides_policy_denies_access(
    access_evaluator: AccessEvaluator, user_deny_policy: IdentifiedPolicy,
    standard_target: PolicyTarget, user_attributes: dict[str, str]
) -> None:
    # Arrange
    access_evaluator._policy_repository.find.return_value.all.return_value = [user_deny_policy]

    # Act
    decision = access_evaluator.evaluate(traget=standard_target, attributes=user_attributes)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.DENY


def test_deny_when_allow_overrides_policy_has_no_matching_rules(
    access_evaluator: AccessEvaluator, guest_policy_with_special_condition: IdentifiedPolicy,
    guest_target: PolicyTarget, guest_attributes: dict[str, str]
) -> None:
    # Arrange
    access_evaluator._policy_repository.find.return_value.all.return_value = [guest_policy_with_special_condition]

    # Act
    decision = access_evaluator.evaluate(traget=guest_target, attributes=guest_attributes)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.DENY


def test_deny_when_deny_overrides_policy_takes_precedence_over_allow_policy(
    access_evaluator: AccessEvaluator, admin_deny_policy: IdentifiedPolicy,
    admin_allow_policy: IdentifiedPolicy, standard_target: PolicyTarget,
    standard_attributes: dict[str, str]
) -> None:
    # Arrange
    access_evaluator._policy_repository.find.return_value.all.return_value = [admin_deny_policy, admin_allow_policy]

    # Act
    decision = access_evaluator.evaluate(traget=standard_target, attributes=standard_attributes)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.DENY


def test_allow_when_allow_overrides_policy_takes_precedence_over_deny_policy(
    access_evaluator: AccessEvaluator, admin_allow_policy: IdentifiedPolicy,
    user_deny_policy: IdentifiedPolicy, standard_target: PolicyTarget,
    standard_attributes: dict[str, str]
) -> None:
    # Arrange
    # In this case, the admin_allow_policy should take precedence because it's ALLOW_OVERRIDES
    # and the attributes match the admin role, not the user role
    access_evaluator._policy_repository.find.return_value.all.return_value = [admin_allow_policy, user_deny_policy]

    # Act
    decision = access_evaluator.evaluate(traget=standard_target, attributes=standard_attributes)

    # Assert
    access_evaluator._policy_repository.find.assert_called_once
    access_evaluator._policy_repository.find.return_value.all.assert_called_once
    assert decision == Decision.ALLOW
