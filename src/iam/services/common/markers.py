from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class Command[TRes](ABC): ...


@dataclass(frozen=True, kw_only=True, slots=True)
class Query[TRes](ABC): ...


class QueryHandler[TQuery: Query, TRes](ABC):
    @abstractmethod
    def handle(self, query: TQuery) -> TRes: ...


class CommandHandler[TCommand: Command, TRes](ABC):
    @abstractmethod
    def handle(self, command: TCommand) -> TRes: ...
