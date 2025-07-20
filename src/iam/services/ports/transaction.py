from abc import ABC, abstractmethod


class Transaction(ABC):
    @abstractmethod
    def commit(self) -> None: ...
    @abstractmethod
    def flush(self) -> None: ...
