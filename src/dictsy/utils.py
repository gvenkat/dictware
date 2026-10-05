from __future__ import annotations

from typing import Any, Hashable


def dig(obj: dict | list, *keys: Hashable) -> Any:
    """Return the value nested in ``obj`` at the path given by ``keys``.

    Mirrors Ruby's ``Hash#dig`` / ``Array#dig``: returns ``None`` as soon as a
    key is missing, an index is out of range, or an intermediate value is
    ``None``. Raises ``TypeError`` if an intermediate value is neither a dict
    nor a list, or if a list is indexed with a non-integer.

        >>> dig({"a": {"b": [10, 20]}}, "a", "b", 1)
        20
        >>> dig({"a": {}}, "a", "missing", "deeper") is None
        True
    """
    current: Any = obj
    for key in keys:
        if current is None:
            return None
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            if not isinstance(key, int) or isinstance(key, bool):
                raise TypeError(
                    f"list indices must be integers, not {type(key).__name__}"
                )
            try:
                current = current[key]
            except IndexError:
                return None
        else:
            raise TypeError(f"{type(current).__name__} does not support dig")
    return current
