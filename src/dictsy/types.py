from typing import Any
from typing import Callable
from typing import TypeAlias

from collections.abc import Hashable

BoolCallback: TypeAlias = Callable[[Hashable, Any], bool]
ValueCallback: TypeAlias = Callable[[Hashable, Any], Any]