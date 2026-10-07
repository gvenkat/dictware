import re
from collections.abc import Hashable
from typing import Any, Callable, Optional

from .types import BoolCallback, ValueCallback


def reduce(d: dict, cb: Callable[[Hashable, Any, Any], Any], memo: Any) -> Any:
  """Cumulatively apply a function on each entry (key, value) of dictionary and an initial value, return the result of cumulative application

  Callback function is invoked for every key, value pair in the dictionary along with result of last application. The
  result is then applied again for the next invocation of the callback, until finally the result is obtained.

  Args:
    d: Dictionary
    cb: Callback accepts three arguments, key, value and memo, the result of last invocation
    memo: Initial value for cumulutive result

  Returns:
    Single value after iterating through the whole dictionary

  Examples:
    >>> reduce({}, lambda key, value, memo: memo)
    0
    >>> reduce({"a": 1, "b": 2}, lambda key, value, memo: memo + value )
    3
    >>> reduce({"a": 1, "b": 2}, lambda key, value, memo: memo + value, 10)
    13
  """
  for key, value in d.items():
    memo = cb(key, value, memo)
  return memo

def select(d: dict, cb: Optional[BoolCallback] = None) -> dict:
  """Returns a new dictionary with entries whose values (or result of callback) are truthy

  Accepts an optional callback function which is called with ``cb(key, value)`` from each entry and
  the return value is tested, when function is not provided, truthiness of values are tested with ``bool(value)``

  Args:
    d: Dictionary
    cb: Callback function accepts two arguments ``key`` and ``value``

  Returns:
    New dictionary with entries whose values (or result of callback) are truthy

  Examples:
    >>> select({})
    {}
    >>> select({"a": "", "b": None})
    {}
    >>> select({"a": "foobar", "b": None})
    {"a": "foobar"}
    >>> select({"a": 5, "b": 2}, lambda key, value: value > 3)
    {"a": 5}
  """
  cb_ = cb or (lambda key, value: bool(value))
  return {key: value for key, value in d.items() if cb_(key, value)}

def reject(d: dict, cb: Optional[BoolCallback] = None) -> dict:
  """Returns a new dictionary with entries that fail the ``cb(key, value)`` test (or value with ``bool(value)`` that is falsy)

  With optional callback function, a new dictionary contains all (key, value) pairs that fails the ``cb(key, value)`` test, without 
  the callback, it returns keys with values that are falsy

  Args:
    d: Dictionary
    cb: Callback function accepts two arguments ``key`` and ``value``

  Returns:
    New dictionary with entries that fail the ``cb(key, value)`` test (or value with ``bool(value)`` that is falsy)

  Examples:
    >>> reject({})
    {}
    >>> reject({"a": "foo"})
    {}
    >>> reject({"a": 2, "b": 5}, lambda key, value: value > 4)
    {"a": 2}
  """
  cb_ = (lambda key, value: not bool(value)) if cb is None else (lambda key, value: not cb(key, value))
  return select(d, cb_)

def transform(d: dict[Hashable, Any], cb: ValueCallback) -> dict:
  """Returns a new dictionary with same keys as the original dictionary, and values returned by invoking the callback function

  Returns a new dictionary with identical keys but values replaced by return value of ``cb(key, value)``

  Args:
    d: Dictionary
    cb: Callback function accepts two arguments ``key`` and ``value`` and returns a new value

  Returns:
    A new dictionary with identical keys and replaced values

  Examples:
    >>> transform({}, lambda key, value: value)
    {}
    >>> transform({"a": 2}, lambda key, value: value * 2)
    {"a": 4}
  """
  return { key: cb(key, value) for key, value in d.items() }

def transform_keys(d: dict, cb: ValueCallback) -> dict:
  return { cb(key, value): value for key, value in d.items() }

def transform_values(d: dict, cb: ValueCallback) -> dict:
  return { key: cb(key, value) for key, value in d.items() }

def delete_if(d: dict, cb: BoolCallback) -> dict:
  return { key: value for key, value in d.items() if not cb(key, value) }

def keep_if(d: dict, cb: BoolCallback) -> dict:
  return delete_if(d, lambda key, value: not cb(key, value))

def grep(d: dict, pattern: re.Pattern):
  pass

def grep_v(d: dict, pattern: re.Pattern):
  pass

def grep_keys(d: dict, pattern: re.Pattern):
  pass

def grep_keys_v(d: dict, pattern: re.Pattern):
  pass

def compact(d: dict, only_none=True) -> dict:
    """Return a new dict with empty values removed from ``d``.

    By default only ``None`` values are removed, like Ruby's ``Hash#compact``.
    With ``only_none=False``, every falsy value is removed: ``None``, ``False``,
    ``0``, ``""``, and empty containers such as ``[]`` and ``{}``.

        >>> compact({"a": 1, "b": None, "c": 0})
        {'a': 1, 'c': 0}
        >>> compact({"a": 1, "b": None, "c": 0}, only_none=False)
        {'a': 1}
    """
    if only_none:
        return {key: value for key, value in d.items() if value is not None}
    return {key: value for key, value in d.items() if value}


def invert(d: dict) -> dict:
    """Return a new dict with the keys and values of ``d`` swapped.

    Entries whose value is not hashable (e.g. lists, dicts, sets) are skipped.
    If several keys share the same value, the last one wins, like Ruby's
    ``Hash#invert``.

        >>> invert({"a": 1, "b": 2})
        {1: 'a', 2: 'b'}
        >>> invert({"a": 1, "b": [2]})
        {1: 'a'}
    """
    inverted = {}
    for key, value in d.items():
        try:
            hash(value)
        except TypeError:
            continue
        inverted[value] = key
    return inverted