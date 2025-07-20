from dataclasses import dataclass, field
from enum import StrEnum, auto


class ErrorType(StrEnum):
    APPLICATION_ERROR = auto()
    UNAUTHORIZED = auto()
    UNAUTHENTICATED = auto()
    NOT_FOUND = auto()
    CONFLICT = auto()


@dataclass(frozen=True, kw_only=True, slots=True)
class ApplicationError(Exception):
    message: str = field(default="An error occurred")
    error_type: ErrorType = field(default=ErrorType.APPLICATION_ERROR)
