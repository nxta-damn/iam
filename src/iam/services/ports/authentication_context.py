from abc import ABC, abstractmethod

from iam.domain.access.session.session_id import SessionIdentity
from iam.domain.shared.user_id import UserIdentity


class AuthenticationContext(ABC):
    @abstractmethod
    def current_user_id(self) -> UserIdentity | None: ...
    @abstractmethod
    def current_session_id(self) -> SessionIdentity | None: ...
