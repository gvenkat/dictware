# dictware

Ruby-inspired helpers for working with Python dicts.

Ruby's `Hash` comes with a rich set of methods (`dig`, `compact`, `select`, `reject`,
`transform_keys`, `grep`, ...). `dictware` brings the same toolkit to plain Python
dictionaries as small, dependency-free functions.

```python
from dictware import dig, select, transform_keys

config = {"db": {"hosts": [{"name": "primary"}, {"name": "replica"}]}}
dig(config, "db", "hosts", 1, "name")          # 'replica'
dig(config, "db", "missing", "key")            # None, no KeyError

select({"a": 5, "b": 2}, lambda k, v: v > 3)    # {'a': 5}
transform_keys({"a": 1}, lambda k, v: k.upper())  # {'A': 1}
```

## Installation

```sh
pip install dictware
```

or with [uv](https://docs.astral.sh/uv/):

```sh
uv add dictware
```

Requires Python 3.10+. No runtime dependencies.

## Conventions

- **Callbacks take `(key, value)`.** Every function that accepts a callback calls it
  as `cb(key, value)` (`reduce` also passes the accumulator: `cb(key, value, memo)`).
- **Non-mutating by default.** Functions return a new dict and leave the input
  untouched. The exceptions are `delete_if` and `keep_if`, which modify the dict in place.
- **Optional callbacks test truthiness.** Where the callback is optional
  (`every`, `some`, `none`, `one`, `select`, `reject`), leaving it out tests each value
  with `bool(value)`.

## API

### Querying

| Function | Description |
| --- | --- |
| `dig(obj, *keys)` | Fetch a nested value from dicts/lists; returns `None` if any step is missing |
| `every(d, cb=None)` | `True` if all values (or `cb(key, value)`) are truthy |
| `some(d, cb=None)` | `True` if any value (or `cb(key, value)`) is truthy |
| `one(d, cb=None)` | `True` if exactly one value (or `cb(key, value)`) is truthy |
| `has_value(d, value_or_cb)` | `True` if `d` contains the value, or any entry passes `cb(key, value)` |

```python
from dictware import dig, every, has_value, one, some

dig({"a": [10, 20]}, "a", 1)                   # 20
dig({"a": [10, 20]}, "a", 5)                   # None

every({"a": 1, "b": 2})                        # True
some({"a": 0, "b": None})                      # False
one({"a": 1, "b": 0})                          # True
every({"a": 5, "b": 10}, lambda k, v: v > 5)   # False

has_value({"a": 1, "b": 2}, 2)                 # True
has_value({"a": 1, "b": 2}, lambda k, v: v > 1)  # True
```

### Filtering

| Function | Description |
| --- | --- |
| `select(d, cb=None)` | Keep entries whose value (or `cb(key, value)`) is truthy |
| `reject(d, cb=None)` | Drop entries whose value (or `cb(key, value)`) is truthy |
| `compact(d, only_none=True)` | Drop `None` values (or all falsy values with `only_none=False`) |
| `grep(d, pattern)` | Keep entries whose `str(value)` matches the regex |
| `grep_v(d, pattern)` | Keep entries whose `str(value)` does not match the regex |
| `grep_keys(d, pattern)` | Keep entries whose `str(key)` matches the regex |
| `grep_keys_v(d, pattern)` | Keep entries whose `str(key)` does not match the regex |

```python
import re
from dictware import compact, grep, grep_keys, reject, select

select({"a": "foo", "b": None})                # {'a': 'foo'}
reject({"a": 2, "b": 5}, lambda k, v: v > 4)   # {'a': 2}

compact({"a": 1, "b": None, "c": 0})                   # {'a': 1, 'c': 0}
compact({"a": 1, "b": None, "c": 0}, only_none=False)  # {'a': 1}

user = {"user_id": 1, "user_name": "bob", "age": 30}
grep_keys(user, re.compile("user_"))           # {'user_id': 1, 'user_name': 'bob'}
grep({"a": "foobar", "b": "barfoo"}, re.compile("foo"))  # {'a': 'foobar'}
```

> **Note:** the `grep` family uses `pattern.match`, which is anchored at the start of
> the string. Prefix the pattern with `.*` to match anywhere.

### Transforming

| Function | Description |
| --- | --- |
| `transform(d, cb)` | Same keys, values replaced by `cb(key, value)` |
| `transform_keys(d, cb)` | Same values, keys replaced by `cb(key, value)` (later keys win on collision) |
| `invert(d)` | Swap keys and values (unhashable values are skipped, later keys win) |
| `reduce(d, cb, memo)` | Fold the dict into a single value with `cb(key, value, memo)` |

```python
from dictware import invert, reduce, transform, transform_keys

prices = {"apple": 2, "pear": 3}
transform(prices, lambda k, v: v * 2)          # {'apple': 4, 'pear': 6}
transform_keys(prices, lambda k, v: k.upper()) # {'APPLE': 2, 'PEAR': 3}
invert(prices)                                 # {2: 'apple', 3: 'pear'}
reduce(prices, lambda k, v, total: total + v, 0)  # 5
```

### Mutating in place

| Function | Description |
| --- | --- |
| `delete_if(d, cb)` | Remove entries where `cb(key, value)` is truthy; returns `d` |
| `keep_if(d, cb)` | Remove entries where `cb(key, value)` is falsy; returns `d` |

```python
from dictware import delete_if

stock = {"apple": 0, "pear": 3}
delete_if(stock, lambda k, v: v == 0)
stock                                          # {'pear': 3}
```

## Development

```sh
uv sync            # install dev dependencies
uv run pytest      # run the test suite
uv run ruff check  # lint
```

## License

TBD
