from abc import ABC
from collections.abc import Hashable
from typing import NoReturn

from iam.domain.shared.events import Event


class IdentifiedEntity[TEntityID: Hashable](ABC):
    def __init__(self, identity: TEntityID) -> None:
        self.identity = identity

    @property
    def identity(self) -> TEntityID:
        return self.identity

    @identity.setter
    def identity(self, identity: TEntityID) -> NoReturn:
        raise AttributeError("Identity is immutable attr")

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
    def __init__(self) -> None:
        self._events: list[Event] = []

    def add_event(self, event: Event) -> None:
        self._events.append(event)

    def raise_events(self) -> list[Event]:
        events = self._events.copy()
        self._events.clear()
        return events
