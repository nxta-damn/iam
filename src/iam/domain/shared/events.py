from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import NewType
from uuid import UUID, uuid4

EventId = NewType("EventId", UUID)


@dataclass(frozen=True, kw_only=True, slots=True)
class Event:
    event_date: datetime = field(default_factory=lambda: datetime.now(UTC), init=False)
    event_id: EventId = field(default_factory=lambda: EventId(uuid4()), init=False)

    @property
    def event_type(self) -> str:
        return type(self).__name__

    def __str__(self) -> str:
        return f"{self.event_type}({self.event_id})"

    def __repr__(self) -> str:
        return f"{self.event_type}({self.event_id})"


class EventHandler[TEvent: Event](ABC):
    @abstractmethod
    def handle(self, event: TEvent) -> None: ...
