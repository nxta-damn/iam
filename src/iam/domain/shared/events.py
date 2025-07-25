from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import NewType
from uuid import UUID

EventId = NewType("EventId", UUID)


@dataclass(frozen=True, kw_only=True, slots=True)
class Event:
    event_date: datetime | None = field(default=None, init=False)
    event_id: EventId | None = field(default=None, init=False)

    def set_event_id(self, event_id: EventId) -> None:
        if not self.event_id:
            object.__setattr__(self, "event_id", event_id)

    def set_event_date(self, event_date: datetime) -> None:
        if not self.event_date:
            object.__setattr__(self, "event_date", event_date)

    @property
    def event_type(self) -> str:
        return type(self).__name__

    def __str__(self) -> str:
        return f"{self.event_type}({self.event_id})"

    def __repr__(self) -> str:
        return f"{self.event_type}({self.event_id})"


class EventTracker(ABC):
    @abstractmethod
    def add_event(self, event: Event) -> None: ...
    @abstractmethod
    def raise_events(self) -> list[Event]: ...


class EventHandler[TEvent: Event](ABC):
    @abstractmethod
    async def handle(self, event: TEvent) -> None: ...
