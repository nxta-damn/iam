from abc import ABC, abstractmethod

from iam.domain.access.session.session import IdentifiedAuthSession
from iam.domain.shared.user_id import UserIdentity


class SessionFactory(ABC):
    @abstractmethod
    def authentificate_user(self, user_id: UserIdentity) -> IdentifiedAuthSession: ...
