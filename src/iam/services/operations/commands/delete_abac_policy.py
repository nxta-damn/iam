from dataclasses import dataclass

import structlog

from iam.domain.access.abac.contracts.policy_repository import PolicyRepository
from iam.domain.access.abac.events import PolicyRemoved
from iam.domain.access.abac.policy_id import PolicyIdentity
from iam.domain.access.abac.specifications import IdentifiedPolicyByIdentitySpec
from iam.domain.identity.contracts.repository import UserRepository
from iam.domain.identity.specifications import IdentifiedUserByIdentitySpec
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Command, CommandHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.event_publisher import EventPublisher
from iam.services.ports.policy_enforcement_point import AuthorizationAttribute, PolicyEnforcementPoint
from iam.services.ports.transaction import Transaction

LOGGER: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass(frozen=True, slots=True, kw_only=True)
class DeleteAbacPolicy(Command[None]):
    policy_identity: PolicyIdentity


class DeleteAbacPolicyHandler(CommandHandler[DeleteAbacPolicy, None]):
    def __init__(
        self,
        authentication_context: AuthenticationContext,
        transaction: Transaction,
        policy_repository: PolicyRepository,
        policy_enforcement_point: PolicyEnforcementPoint,
        event_publisher: EventPublisher,
        user_repository: UserRepository,
    ) -> None:
        self._authentication_context = authentication_context
        self._transaction = transaction
        self._policy_repository = policy_repository
        self._policy_enforcement_point = policy_enforcement_point
        self._event_publisher = event_publisher
        self._user_repository = user_repository

    def handle(self, command: DeleteAbacPolicy) -> None:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        user_by_identity_spec = IdentifiedUserByIdentitySpec(identity=current_user_id)
        current_user = self._user_repository.find(user_by_identity_spec).first()

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        is_authorized = self._policy_enforcement_point.authorize(
            action=AuthorizationAttribute(target_name="action", attributes={"name": "delete_abac_policy"}),
            subject=AuthorizationAttribute(
                target_name="user", attributes={"user_type": current_user.user_type}
            ),
            resource=AuthorizationAttribute(target_name="abac-policy", attributes={}),
        )

        if not is_authorized:
            raise ApplicationError(
                message="User is not authorized to delete abac policy", error_type=ErrorType.UNAUTHORIZED
            )

        policy_by_identity_spec = IdentifiedPolicyByIdentitySpec(identity=command.policy_identity)
        policy = self._policy_repository.find(policy_by_identity_spec).first()

        if not policy:
            raise ApplicationError(
                message=f"Policy with id: {command.policy_identity} is not found",
                error_type=ErrorType.NOT_FOUND,
            )

        policy.add_event(event=PolicyRemoved(identity=command.policy_identity))

        for event in policy.raise_events():
            self._event_publisher.publish(event=event)

        self._policy_repository.delete(policy)
        self._transaction.commit()

        LOGGER.info(
            "Abac policy deleted", policy_identity=command.policy_identity, current_user=current_user_id
        )
