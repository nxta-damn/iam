from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class AuthorizationAttribute:
    target_name: str
    attributes: dict[str, str | int | list]


class PolicyEnforcementPoint(ABC):
    @abstractmethod
    def authorize(
        self,
        resource: AuthorizationAttribute | None = None,
        action: AuthorizationAttribute | None = None,
        subject: AuthorizationAttribute | None = None,
        environment: AuthorizationAttribute | None = None,
    ) -> bool: ...
