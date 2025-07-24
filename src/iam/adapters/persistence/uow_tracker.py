from abc import ABC, abstractmethod


class UoWTracker[ModelT](ABC):
    @abstractmethod
    def register_dirty(self, model: ModelT) -> None: ...
    @abstractmethod
    def register_new(self, model: ModelT) -> None: ...
    @abstractmethod
    def register_deleted(self, model: ModelT) -> None: ...
