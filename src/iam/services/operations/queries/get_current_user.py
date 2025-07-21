from dataclasses import dataclass

from iam.services.common.application_error import ApplicationError, ErrorType
from iam.services.common.markers import Query, QueryHandler
from iam.services.models.user import UserReadModel
from iam.services.ports.authentication_context import AuthenticationContext
from iam.services.ports.user_gateway import UserGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class GetCurrentUser(Query[UserReadModel]): ...


class GetCurrentUserHandler(QueryHandler[GetCurrentUser, UserReadModel]):
    def __init__(
        self,
        user_gateway: UserGateway,
        authentication_context: AuthenticationContext,
    ) -> None:
        self._user_gateway = user_gateway
        self._authentication_context = authentication_context

    async def handle(self, query: GetCurrentUser) -> UserReadModel:
        current_user_id = self._authentication_context.current_user_id()

        if not current_user_id:
            raise ApplicationError(message="User is not authenticated", error_type=ErrorType.UNAUTHENTICATED)

        current_user = await self._user_gateway.with_id(user_id=current_user_id)

        if not current_user:
            raise ApplicationError(
                message=f"User with id: {current_user_id} is not found", error_type=ErrorType.NOT_FOUND
            )

        return current_user
