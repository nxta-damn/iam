from abc import ABC, abstractmethod
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, kw_only=True, slots=True)
class Command[TRes](ABC): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class Query[TRes](ABC): ...


class QueryHandler[TQuery: Query, TRes](ABC):
    @abstractmethod
    async def handle(self, query: TQuery) -> TRes: ...


class CommandHandler[TCommand: Command, TRes](ABC):
    @abstractmethod
    async def handle(self, command: TCommand) -> TRes: ...


class Middleware[TReq, TRes](ABC):
    @abstractmethod
    async def handle(self, request: TReq, process: Callable[[TReq], Coroutine[Any, Any, TRes]]) -> TRes: ...
