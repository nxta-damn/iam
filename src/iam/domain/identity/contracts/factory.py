from abc import ABC, abstractmethod

from iam.domain.identity.user import IdentifiedUser
from iam.domain.identity.value_objects.fullname import Fullname


class UserFactory(ABC):
    @abstractmethod
    def create_user(
        self,
        fullname: Fullname,
        username: str,
        password: bytes,
    ) -> IdentifiedUser: ...
