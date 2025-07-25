from abc import ABC, abstractmethod

from iam.domain.access.session_id import SessionIdentity
from iam.domain.shared.events import EventId
from iam.domain.shared.user_id import UserIdentity


class IdProvider(ABC):
    @abstractmethod
    def generate_session_id(self) -> SessionIdentity: ...
    @abstractmethod
    def generate_event_id(self) -> EventId: ...
    @abstractmethod
    def generate_user_id(self) -> UserIdentity: ...
