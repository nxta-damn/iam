from iam.domain.access.abac.operators.operator import Operator


class Equals(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr == self.value


class Gt(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr > self.value


class Gte(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr >= self.value


class Lt(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr < self.value


class Lte(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr <= self.value


class Neq(Operator[int]):
    def __init__(self, value: int) -> None:
        self.value = value

    def is_satisfied(self, attr: int) -> bool:
        return attr != self.value
