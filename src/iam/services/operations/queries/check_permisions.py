from dataclasses import dataclass, field

from iam.domain.access.abac.services.access_evaluator import Decision
from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Query, QueryHandler
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.policy_enforcement_point import AuthorizationAttribute, PolicyEnforcementPoint
from iam.services.ports.user_gateway import UserGateway


@dataclass(frozen=True, kw_only=True, slots=True)
class CheckPermissions(Query[Decision]):
    action: AuthorizationAttribute | None = field(default=None)
    resourse: AuthorizationAttribute | None = field(default=None)
    subject: AuthorizationAttribute | None = field(default=None)
    environment: AuthorizationAttribute | None = field(default=None)


class CheckPermissionsHandler(QueryHandler[CheckPermissions, Decision]):
    def __init__(
        self,
        authentication_context: AuthenticationContext,
        policy_enforcement_point: PolicyEnforcementPoint,
        user_gateway: UserGateway,
    ) -> None:
        self._authentication_context = authentication_context
        self._policy_enforcement_point = policy_enforcement_point
        self._user_gateway = user_gateway

    def handle(self, query: CheckPermissions) -> Decision:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_user = self._user_gateway.with_id(user_id=current_user_id)

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        decision = self._policy_enforcement_point.authorize(
            resource=query.resourse, action=query.action, subject=query.action, environment=query.environment
        )

        return Decision.ALLOW if decision else Decision.DENY
