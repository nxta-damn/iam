from abc import ABC, abstractmethod


class DataMapper[ModelT](ABC):
    @abstractmethod
    async def insert(self, model: ModelT) -> None: ...
    @abstractmethod
    async def update(self, model: ModelT) -> None: ...
    @abstractmethod
    async def delete(self, model: ModelT) -> None: ...
