from collections.abc import Collection

from iam.domain.access.abac.operators.operator import Operator


class In(Operator[Collection[str]]):
    def __init__(self, values: Collection[str]) -> None:
        self.values = values

    def is_satisfied(self, attr: Collection[str]) -> bool:
        return attr in self.values


class NotIn(Operator[Collection[str]]):
    def __init__(self, values: Collection[str]) -> None:
        self.values = values

    def is_satisfied(self, attr: Collection[str]) -> bool:
        return attr not in self.values


class IsEmpty(Operator[Collection[str]]):
    def is_satisfied(self, attr: Collection[str]) -> bool:
        return len(attr) == 0


class IsNotEmpty(Operator[Collection]):
    def is_satisfied(self, attr: Collection[str]) -> bool:
        return len(attr) > 0
