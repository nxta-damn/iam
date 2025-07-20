from dataclasses import dataclass

from iam.domain.identity.contracts.repository import UserRepository
from iam.domain.identity.specifications import IdentifiedUserByIdentitySpec
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Query, QueryHandler
from iam.services.models.abac_policy import AbacPolicyReadModel
from iam.services.models.pagination import Pagination
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.policy_enforcement_point import AuthorizationAttribute, PolicyEnforcementPoint
from iam.services.ports.policy_gateway import AbacPolicyGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class GetPaginatedAbacPolicies(Query[list[AbacPolicyReadModel]]):
    pagination: Pagination


class GetPaginatedPoliciesHandler(QueryHandler[GetPaginatedAbacPolicies, list[AbacPolicyReadModel]]):
    def __init__(
        self,
        policy_gateway: AbacPolicyGateway,
        authentication_context: AuthenticationContext,
        policy_enforcement_point: PolicyEnforcementPoint,
        user_repository: UserRepository,
    ) -> None:
        self._policy_gateway = policy_gateway
        self._authentication_context = authentication_context
        self._policy_enforcement_point = policy_enforcement_point
        self._user_repository = user_repository

    def handle(self, query: GetPaginatedAbacPolicies) -> list[AbacPolicyReadModel]:
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
            action=AuthorizationAttribute(target_name="action", attributes={"name": "get_policies"}),
            subject=AuthorizationAttribute(
                target_name="user", attributes={"user_type": current_user.user_type}
            ),
            resource=AuthorizationAttribute(target_name="abac-policy", attributes={}),
        )

        if not is_authorized:
            raise ApplicationError(
                message="User is not authorized to get abac policies", error_type=ErrorType.UNAUTHORIZED
            )

        abac_policies = self._policy_gateway.load_many(pagination=query.pagination)

        return abac_policies
