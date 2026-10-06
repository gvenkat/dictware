from typing import TypeAlias
from typing import Callable
from typing import Hashable
from typing import Any

BoolCallback: TypeAlias = Callable[[Hashable, Any], bool]
ValueCallback: TypeAlias = Callable[[Hashable, Any], Any]