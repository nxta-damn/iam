from abc import ABC, abstractmethod

from iam.domain.shared.events import Event


class EventPublisher(ABC):
    @abstractmethod
    async def publish(self, event: Event) -> None: ...
