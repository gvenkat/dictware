from collections.abc import Hashable
from typing import Any, Callable, TypeAlias

BoolCallback: TypeAlias = Callable[[Hashable, Any], bool]
ValueCallback: TypeAlias = Callable[[Hashable, Any], Any]