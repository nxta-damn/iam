from collections.abc import Callable
from typing import Any, Final

from iam.domain.access.abac.operators.collection import In, IsEmpty, IsNotEmpty, NotIn
from iam.domain.access.abac.operators.numeric import Equals, Gt, Gte, Lt, Lte, Neq
from iam.domain.access.abac.operators.operator import Operator
from iam.domain.access.abac.operators.string import Contains, EndsWidth, Eq, NotContains, NotEq, StarsWith

OPERATORS_MAP: Final[dict[tuple[str, str], Callable[[Any], Operator]]] = {
    ("string", "eq"): lambda v: Eq(v),
    ("string", "not_eq"): lambda v: NotEq(v),
    ("string", "starts_with"): lambda v: StarsWith(v),
    ("string", "ends_with"): lambda v: EndsWidth(v),
    ("string", "contains"): lambda v: Contains(v),
    ("string", "not_contains"): lambda v: NotContains(v),
    ("numeric", "eq"): lambda v: Equals(v),
    ("numeric", "gt"): lambda v: Gt(v),
    ("numeric", "gte"): lambda v: Gte(v),
    ("numeric", "lt"): lambda v: Lt(v),
    ("numeric", "lte"): lambda v: Lte(v),
    ("numeric", "neq"): lambda v: Neq(v),
    ("collection", "in"): lambda v: In(v),
    ("collection", "not_in"): lambda v: NotIn(v),
    ("collection", "is_empty"): lambda v: IsEmpty(),
    ("collection", "is_not_empty"): lambda v: IsNotEmpty(),
}
