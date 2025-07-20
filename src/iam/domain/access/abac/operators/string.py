from iam.domain.access.abac.operators.operator import Operator


class Eq(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return attr == self.value


class NotEq(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return attr != self.value


class StarsWith(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return attr.startswith(self.value)


class EndsWidth(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return attr.endswith(self.value)


class Contains(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return self.value in attr


class NotContains(Operator[str]):
    def __init__(self, value: str) -> None:
        self.value = value

    def is_satisfied(self, attr: str) -> bool:
        return self.value not in attr
