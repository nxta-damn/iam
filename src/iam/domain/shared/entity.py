from abc import ABC
from collections.abc import Hashable
from typing import NoReturn

from iam.domain.shared.events import DomainEvent, DomainEventAdder


class IdentifiedEntity[TEntityID: Hashable](ABC):
    def __init__(self, identity: TEntityID) -> None:
        self._identity = identity

    @property
    def identity(self) -> TEntityID:
        return self._identity

    @identity.setter
    def identity(self, identity: TEntityID) -> NoReturn:
        raise AttributeError("Identity is immutable attr")

    def __hash__(self) -> int:
        return hash(self._identity)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IdentifiedEntity):
            return NotImplemented
        return bool(self._identity == other._identity)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._identity})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._identity})"


class EventTrackableEntity(ABC):
    def __init__(self, event_adder: DomainEventAdder) -> None:
        self._event_adder = event_adder

    def add_event(self, event: DomainEvent) -> None:
        self._event_adder.add_event(event)
