from __future__ import annotations

import builtins
from collections.abc import Hashable
from typing import Any

from .types import BoolCallback


def every(d: dict, cb: BoolCallback | None = None) -> bool:
  """Returns ``True`` if ALL values in the ``dict`` are ``True``

  Returns ``True`` if ALL values in a given dict is "truthy" or ALL the values evaulated by
  the optional callback is "truthy"

  Args:
    d: The dict object
    cb: If callback is given, result of ``cb(key, value)`` is considered, if not ``value`` is tested
        directly for truthiness

  Returns:
    True if every value (or ``cb(key, value)``) is evaluated to True. False otherwise

  Examples:
    >>> all({})
    True
    >>> all({"a": 1, "b": 2})
    True
    >>> all({"a": 1, "b": None})
    False
    >>> all({"a": 1, "b": 5}, lambda k, v: v > 0)
    False
  """

  if cb is None:
    return builtins.all(d.values())

  for key, value in d.items():
    if not cb(key, value):
      return False

  return True


def some(d: dict, cb: BoolCallback | None = None) -> bool:
  """Returns ``True`` if ANY of the values in the ``dict`` are ``True``

  Returns ``True`` if ANY of the values in a given dict is "truthy" or ANY the values evaulated by
  the optional callback is "truthy"

  Args:
    d: The dict object
    cb: If callback is given, result of ``cb(key, value)`` is considered, if not ``value`` is tested
        directly for truthiness

  Returns:
    True if any value (or ``cb(key, value)``) is evaluated to True. False otherwise

  Examples:
    >>> any({})
    False
    >>> any({"a": 1, "b": 2})
    True
    >>> any({"a": 1, "b": None})
    True
    >>> any({"a": [], "b": None})
    False
    >>> any({"a": 1, "b": 5}, lambda k, v: v > 2)
    True
  """
  if cb is None:
    return builtins.any(d.values())

  for key, value in d.items():
    if cb(key, value):
      return True

  return False

def none(d: dict, cb: BoolCallback | None = None) -> bool:
  """Returns ``True`` if NONE of the values are truthy

  Returns ``True`` if NONE of the values in a given dict is "truthy" or NONE of the values evaulated by
  the optional callback is "truthy"

  Args:
    d: The dict object
    cb: If callback is given, result of ``cb(key, value)`` is considered, if not ``value`` is tested
        directly for truthiness

  Returns:
    True if NONE of the values (or ``cb(key, value)``) is evaluated to True. False otherwise
  """
  return not some(d, cb)

def one(d: dict, cb: BoolCallback | None = None) -> bool:
  """Returns ``True`` if EXACTLY ONE of the values is truthy

  Returns ``True`` if exactly one value in a given dict is "truthy" or exactly one of the values evaluated by
  the optional callback is "truthy"

  Args:
    d: The dict object
    cb: If callback is given, result of ``cb(key, value)`` is considered, if not ``value`` is tested
        directly for truthiness

  Returns:
    True if exactly one value (or ``cb(key, value)``) is evaluated to True. False otherwise

  Examples:
    >>> one({})
    False
    >>> one({"a": 1, "b": None})
    True
    >>> one({"a": 1, "b": 2})
    False
    >>> one({"a": 1, "b": 5}, lambda k, v: v > 2)
    True
  """
  return [bool(value if cb is None else cb(key, value)) for key, value in d.items()].count(True) == 1

def has_value(d: dict, value_or_cb: Any | BoolCallback) -> bool:
  """Returns ``True`` if the dict contains the given value, or any entry passes the callback test

  When ``value_or_cb`` is callable, it is called as ``cb(key, value)`` for each entry and ``True`` is returned
  as soon as it returns a truthy value. Otherwise each value is compared with ``value == value_or_cb``.

  Note: a callable is always treated as a callback, so to look for a function stored as a value use
  ``has_value(d, lambda k, v: v is func)``

  Args:
    d: The dict object
    value_or_cb: Value to look for, or callback function accepting ``key`` and ``value``

  Returns:
    True if any value equals ``value_or_cb`` (or ``cb(key, value)`` is truthy). False otherwise

  Examples:
    >>> has_value({}, 1)
    False
    >>> has_value({"a": 1, "b": 2}, 2)
    True
    >>> has_value({"a": 1, "b": 2}, "a")
    False
    >>> has_value({"a": 1, "b": 2}, lambda k, v: v > 1)
    True
  """
  if callable(value_or_cb):
    return builtins.any(value_or_cb(key, value) for key, value in d.items())
  return value_or_cb in d.values()


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
