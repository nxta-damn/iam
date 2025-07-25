from abc import ABC
from collections.abc import Hashable

from iam.domain.shared.events import Event, EventTracker


class IdentifiedEntity[TEntityID: Hashable](ABC):
    def __init__(self, identity: TEntityID) -> None:
        self.identity = identity

    def __hash__(self) -> int:
        return hash(self.identity)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IdentifiedEntity):
            return NotImplemented
        return bool(self.identity == other.identity)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.identity})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.identity})"


class EventTrackableEntity(ABC):
    def __init__(self, event_tracker: EventTracker) -> None:
        self.event_tracker = event_tracker

    def add_event(self, event: Event) -> None:
        self.event_tracker.add_event(event)

    def raise_events(self) -> list[Event]:
        return self.event_tracker.raise_events()
