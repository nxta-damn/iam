from dataclasses import dataclass

import structlog

from iam.domain.access.abac.abac_policy import PolicyAlghorithm
from iam.domain.access.abac.contracts.policy_repository import PolicyRepository
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
class ChangePolicyAlgorithm(Command[None]):
    policy_identity: PolicyIdentity
    algorithm: PolicyAlghorithm


class ChangePolicyAlghorithmHandler(CommandHandler[ChangePolicyAlgorithm, None]):
    def __init__(
        self,
        transaction: Transaction,
        user_repository: UserRepository,
        policy_enforcement_point: PolicyEnforcementPoint,
        authentication_context: AuthenticationContext,
        event_publisher: EventPublisher,
        policy_repository: PolicyRepository,
    ) -> None:
        self._transaction = transaction
        self._user_repository = user_repository
        self._policy_enforcement_point = policy_enforcement_point
        self._authentication_context = authentication_context
        self._event_publisher = event_publisher
        self._policy_repository = policy_repository

    def handle(self, command: ChangePolicyAlgorithm) -> None:
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
            action=AuthorizationAttribute(
                target_name="action", attributes={"name": "change_policy_algorithm"}
            ),
            subject=AuthorizationAttribute(
                target_name="user", attributes={"user_type": current_user.user_type}
            ),
            resource=AuthorizationAttribute(target_name="abac-policy", attributes={}),
        )

        if not is_authorized:
            raise ApplicationError(
                message="User is not authorized to change policy algorithm", error_type=ErrorType.UNAUTHORIZED
            )

        policy_by_identity_spec = IdentifiedPolicyByIdentitySpec(identity=command.policy_identity)
        policy = self._policy_repository.find(policy_by_identity_spec).first()

        if not policy:
            raise ApplicationError(
                message=f"Policy with id: {command.policy_identity} is not found",
                error_type=ErrorType.NOT_FOUND,
            )

        policy.change_alghorithm(alghorithm=command.algorithm)

        for event in policy.raise_events():
            self._event_publisher.publish(event=event)

        self._transaction.commit()

        LOGGER.info(
            "Policy algorithm changed", policy_identity=command.policy_identity, current_user=current_user_id
        )
