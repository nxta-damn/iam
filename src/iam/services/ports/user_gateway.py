from abc import ABC, abstractmethod

from iam.domain.shared.user_id import UserIdentity
from iam.services.models.pagination import Pagination
from iam.services.models.user import UserReadModel


class UserGateway(ABC):
    @abstractmethod
    def with_id(self, user_id: UserIdentity) -> UserReadModel | None: ...
    @abstractmethod
    def load_many(self, pagination: Pagination) -> list[UserReadModel]: ...
