from typing import Optional, Any, Hashable

from .types import BoolCallback

def all(d: dict, cb: Optional[BoolCallback] = None) -> bool:
  """Returns ``True`` if all values in the ``dict`` are ``True``

  Returns ``True`` if all values in a given dict is "truthy" or all the values evaulated by
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

  for key, value in d.items():
    if cb is not None and not cb(key, value):
      return False

    if cb is None and not bool(value):
      return False

  return True


def any(d: dict, cb: Optional[BoolCallback] = None) -> bool:
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
  for key, value in d.items():
    if cb is not None and cb(key, value):
      return True

    if cb is None and bool(value) is True:
      return True

  return False

def none(d: dict, cb: Optional[BoolCallback] = None) -> bool:
  pass

def one(d: dict, cb: Optional[BoolCallback] = None) -> bool:
  pass

def has_value(d: dict, value_or_cb: Any | Optional[BoolCallback]) -> bool:
  pass

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
