from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class ResourceTarget:
    resource_name: str

    def __str__(self) -> str:
        return f"{self.resource_name}"

    def __repr__(self) -> str:
        return f"ResourceTarget({self.resource_name})"


@dataclass(frozen=True, kw_only=True, slots=True)
class ActionTarget:
    action_name: str

    def __str__(self) -> str:
        return f"{self.action_name}"

    def __repr__(self) -> str:
        return f"ActionTarget({self.action_name})"


@dataclass(frozen=True, kw_only=True, slots=True)
class SubjectTarget:
    subject_name: str

    def __str__(self) -> str:
        return f"{self.subject_name}"

    def __repr__(self) -> str:
        return f"SubjectTarget({self.subject_name})"


@dataclass(frozen=True, kw_only=True, slots=True)
class EnvironmentTarget:
    environment_name: str

    def __str__(self) -> str:
        return f"{self.environment_name}"

    def __repr__(self) -> str:
        return f"EnvironmentTarget({self.environment_name})"


@dataclass(frozen=True, kw_only=True, slots=True)
class PolicyTarget:
    subjects: list[SubjectTarget]
    resources: list[ResourceTarget]
    actions: list[ActionTarget]
    environments: list[EnvironmentTarget]

    def __str__(self) -> str:
        return f"{self.subjects}, {self.resources}, {self.actions}, {self.environments}"

    def __repr__(self) -> str:
        return f"PolicyTarget({self.subjects}, {self.resources}, {self.actions}, {self.environments}"
