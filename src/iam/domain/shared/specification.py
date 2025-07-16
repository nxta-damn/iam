from abc import ABC, abstractmethod

from iam.domain.shared.entity import IdentifiedEntity


class Specification[EntityT: IdentifiedEntity](ABC):
    @abstractmethod
    def is_satisfied_by(self, entity: EntityT | None = None) -> bool: ...

    def __invert__(self) -> "Specification[EntityT]":
        return NotSpecification(self)

    def __and__(self, other: "Specification[EntityT]") -> "Specification[EntityT]":
        return AndSpecification(self, other)

    def __or__(self, other: "Specification[EntityT]") -> "Specification[EntityT]":
        return OrSpecification(self, other)


class NotSpecification[EntityT: IdentifiedEntity](Specification[EntityT]):
    def __init__(self, specification: Specification[EntityT]) -> None:
        self._specification = specification

    def is_satisfied_by(self, entity: EntityT | None = None) -> bool:
        return not self._specification.is_satisfied_by(entity=entity)


class AndSpecification[EntityT: IdentifiedEntity](Specification[EntityT]):
    def __init__(self, left: Specification[EntityT], right: Specification[EntityT]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, entity: EntityT | None = None) -> bool:
        return self._left.is_satisfied_by(entity=entity) and self._right.is_satisfied_by(entity=entity)


class OrSpecification[EntityT: IdentifiedEntity](Specification[EntityT]):
    def __init__(self, left: Specification[EntityT], right: Specification[EntityT]) -> None:
        self._left = left
        self._right = right

    def is_satisfied_by(self, entity: EntityT | None = None) -> bool:
        return self._left.is_satisfied_by(entity=entity) or self._right.is_satisfied_by(entity=entity)


class SpecificatedResult[EntityT: IdentifiedEntity](ABC):
    @abstractmethod
    def all(self) -> list[EntityT]: ...
    @abstractmethod
    def first(self) -> EntityT | None: ...
