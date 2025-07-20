from dataclasses import dataclass

from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Query, QueryHandler
from iam.services.models.pagination import Pagination
from iam.services.models.session import SessionReadModel
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.session_gateway import SessionGateway
from iam.services.ports.user_gateway import UserGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserSessions(Query[list[SessionReadModel]]):
    pagination: Pagination


class GetUserSessionsHandler(QueryHandler[GetUserSessions, list[SessionReadModel]]):
    def __init__(
        self,
        session_gateway: SessionGateway,
        authentication_context: AuthenticationContext,
        user_gateway: UserGateway,
    ) -> None:
        self._session_gateway = session_gateway
        self._authentication_context = authentication_context
        self._user_gateway = user_gateway

    def handle(self, query: GetUserSessions) -> list[SessionReadModel]:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_user = self._user_gateway.with_id(user_id=current_user_id)

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        user_sessions = self._session_gateway.with_user_id(current_user_id, query.pagination)

        return user_sessions
