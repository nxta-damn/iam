from abc import ABC, abstractmethod

from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity
from iam.services.models.pagination import Pagination
from iam.services.models.session import SessionReadModel


class SessionGateway(ABC):
    @abstractmethod
    async def with_id(self, session_id: SessionIdentity) -> SessionReadModel | None: ...
    @abstractmethod
    async def with_user_id(self, user_id: UserIdentity, pagination: Pagination) -> list[SessionReadModel]: ...
