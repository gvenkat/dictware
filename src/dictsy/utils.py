from __future__ import annotations

from typing import Any, Hashable, Callable, Any

def all(obj: dict, cb: None | Callable[[Hashable, Any], bool] = None) -> dict[Hashable, Any]:
    """Returns ``True`` if all bool(value) or bool(cb(value)) of all values are ``True``
    """
    return all([bool(value) if cb is not None else bool(cb(key, value)) for key, value in obj.items()])

def any(obj: dict, cb: Callable[[Hashable, Any], bool]) -> dict[Hashable, Any]:
    return any([bool(value) if cb is not None else bool(cb(key, value)) for key, value in obj.items()])

def one():
    pass

def none():
    pass

def delete_if():
    pass

def keep_if():
    pass

def has_value():
    pass

def reject():
    pass

def reject_if():
    pass

def grep():
    pass

def grep_v():
    pass

def filter():
    pass

def map():
    pass

def transform_keys():
    pass

def transform_values():
    pass

def reduce():
    pass



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
