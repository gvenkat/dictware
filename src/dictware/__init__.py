"""Ruby-inspired helpers for working with Python dicts"""
from importlib.metadata import version

__version__ = version('dictware')

from .query import dig, every, has_value, one, some
from .transform import (
  compact,
  delete_if,
  grep,
  grep_keys,
  grep_keys_v,
  grep_v,
  invert,
  keep_if,
  reduce,
  reject,
  select,
  transform,
  transform_keys,
)
