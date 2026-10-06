from typing import Optional

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