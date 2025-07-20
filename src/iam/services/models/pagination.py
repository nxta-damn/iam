from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination:
    limit: int = field(default=10)
    offset: int = field(default=0)
