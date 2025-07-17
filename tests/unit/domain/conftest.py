from unittest.mock import create_autospec
from uuid import uuid4

from pytest import fixture

from iam.domain.access.abac.abac_policy import IdentifiedPolicy, PolicyAlghorithm
from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.value_objects.policy_attribute import AttributeType, PolicyAttribute
from iam.domain.access.abac.value_objects.policy_condition import (
    Action, Environment, PolicyCondition, Resource, Subject
)
from iam.domain.access.abac.value_objects.policy_rule import PolicyRule, RuleEffect
from iam.domain.access.abac.value_objects.policy_target import (
    ActionTarget, EnvironmentTarget, PolicyTarget, ResourceTarget, SubjectTarget
)
from iam.domain.shared.events import DomainEventAdder


@fixture(scope='function')
def event_adder() -> DomainEventAdder:
    return create_autospec(DomainEventAdder)


@fixture(scope='function')
def admin_role_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="role",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="admin"
    )


@fixture(scope='function')
def user_role_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="role",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="user"
    )


@fixture(scope='function')
def guest_role_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="role",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="guest"
    )


@fixture(scope='function')
def read_action_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="action",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="read"
    )


@fixture(scope='function')
def document_resource_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="resource",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="document"
    )


@fixture(scope='function')
def production_env_attribute() -> PolicyAttribute:
    return PolicyAttribute(
        attribute_name="environment",
        attribute_type=AttributeType.STRING,
        operator="eq",
        value="production"
    )


@fixture(scope='function')
def standard_target() -> PolicyTarget:
    return PolicyTarget(
        subjects=[SubjectTarget(subject_name="user")],
        resources=[ResourceTarget(resource_name="document")],
        actions=[ActionTarget(action_name="read")],
        environments=[EnvironmentTarget(environment_name="production")]
    )


@fixture(scope='function')
def guest_target() -> PolicyTarget:
    return PolicyTarget(
        subjects=[SubjectTarget(subject_name="guest")],
        resources=[ResourceTarget(resource_name="document")],
        actions=[ActionTarget(action_name="read")],
        environments=[EnvironmentTarget(environment_name="production")]
    )


@fixture(scope='function')
def standard_attributes() -> dict[str, str]:
    return {'role': 'admin', 'action': 'read', 'resource': 'document', 'environment': 'production'}


@fixture(scope='function')
def user_attributes() -> dict[str, str]:
    return {'role': 'user', 'action': 'read', 'resource': 'document', 'environment': 'production'}


@fixture(scope='function')
def guest_attributes() -> dict[str, str]:
    return {'role': 'guest', 'action': 'read', 'resource': 'document', 'environment': 'production'}


@fixture(scope='function')
def admin_allow_policy(
    event_adder: DomainEventAdder, standard_target: PolicyTarget,
    admin_role_attribute: PolicyAttribute, read_action_attribute: PolicyAttribute,
    document_resource_attribute: PolicyAttribute, production_env_attribute: PolicyAttribute
) -> IdentifiedPolicy:
    return IdentifiedPolicy(
        identity=PolicyIdentity(uuid4()),
        event_adder=event_adder,
        description="Allow admins to read documents",
        target=standard_target,
        rules=[
            PolicyRule(
                name="admin-read-rule",
                effect=RuleEffect.PERMIT,
                conditions=[
                    PolicyCondition(
                        subject=Subject(attributes=[admin_role_attribute]),
                        action=Action(attributes=[read_action_attribute]),
                        resource=Resource(attributes=[document_resource_attribute]),
                        environment=Environment(attributes=[production_env_attribute])
                    )
                ]
            )
        ],
        alghorithm=PolicyAlghorithm.ALLOW_OVERRIDES
    )


@fixture(scope='function')
def user_deny_policy(
    event_adder: DomainEventAdder, standard_target: PolicyTarget,
    user_role_attribute: PolicyAttribute, read_action_attribute: PolicyAttribute,
    document_resource_attribute: PolicyAttribute, production_env_attribute: PolicyAttribute
) -> IdentifiedPolicy:
    return IdentifiedPolicy(
        identity=PolicyIdentity(uuid4()),
        event_adder=event_adder,
        description="Deny users from reading documents",
        target=standard_target,
        rules=[
            PolicyRule(
                name="user-deny-read-rule",
                effect=RuleEffect.DENY,
                conditions=[
                    PolicyCondition(
                        subject=Subject(attributes=[user_role_attribute]),
                        action=Action(attributes=[read_action_attribute]),
                        resource=Resource(attributes=[document_resource_attribute]),
                        environment=Environment(attributes=[production_env_attribute])
                    )
                ]
            )
        ],
        alghorithm=PolicyAlghorithm.DENY_OVERRIDES
    )


@fixture(scope='function')
def guest_policy_with_special_condition(
    event_adder: DomainEventAdder, guest_target: PolicyTarget,
    read_action_attribute: PolicyAttribute, document_resource_attribute: PolicyAttribute,
    production_env_attribute: PolicyAttribute
) -> IdentifiedPolicy:
    return IdentifiedPolicy(
        identity=PolicyIdentity(uuid4()),
        event_adder=event_adder,
        description="Allow only specific guests to read documents",
        target=guest_target,
        rules=[
            PolicyRule(
                name="specific-guest-read-rule",
                effect=RuleEffect.PERMIT,
                conditions=[
                    PolicyCondition(
                        # This condition won't match because we're looking for a different role
                        subject=Subject(attributes=[PolicyAttribute(
                            attribute_name="role",
                            attribute_type=AttributeType.STRING,
                            operator="eq",
                            value="special-guest"
                        )]),
                        action=Action(attributes=[read_action_attribute]),
                        resource=Resource(attributes=[document_resource_attribute]),
                        environment=Environment(attributes=[production_env_attribute])
                    )
                ]
            )
        ],
        alghorithm=PolicyAlghorithm.ALLOW_OVERRIDES
    )


@fixture(scope='function')
def admin_deny_policy(
    event_adder: DomainEventAdder, standard_target: PolicyTarget,
    admin_role_attribute: PolicyAttribute, read_action_attribute: PolicyAttribute,
    document_resource_attribute: PolicyAttribute, production_env_attribute: PolicyAttribute
) -> IdentifiedPolicy:
    return IdentifiedPolicy(
        identity=PolicyIdentity(uuid4()),
        event_adder=event_adder,
        description="Deny all access to documents",
        target=standard_target,
        rules=[
            PolicyRule(
                name="deny-all-rule",
                effect=RuleEffect.DENY,
                conditions=[
                    PolicyCondition(
                        subject=Subject(attributes=[admin_role_attribute]),
                        action=Action(attributes=[read_action_attribute]),
                        resource=Resource(attributes=[document_resource_attribute]),
                        environment=Environment(attributes=[production_env_attribute])
                    )
                ]
            )
        ],
        alghorithm=PolicyAlghorithm.DENY_OVERRIDES
    )
