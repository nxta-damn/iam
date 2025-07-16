from abc import ABC, abstractmethod


class Operator[AttrT](ABC):
    @abstractmethod
    def is_satisfied(self, attr: AttrT) -> bool: ...
