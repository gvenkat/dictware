from typing import TypeAlias, Callable, Hashable, Any

BoolCallback: TypeAlias = Callable[[Hashable, Any], bool]