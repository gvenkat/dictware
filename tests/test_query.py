import pytest

from dictsy import all

@pytest.mark.parametrize(
  'd, expected',
  [
    [{"a": 1, "b": None}, False],
    [{"a": 1, "b": ''}, False],
    [{"a": 1, "b": 0}, False],
    [{"a": 1, "b": []}, False],
    [{"a": 1, "b": False}, False],
    [{"a": 1, "b": True}, True],
    [{"a": 1, "b": "blah"}, True],
  ]
)
def test_all_no_callback(d, expected):
  assert(all(d) == expected)


def test_all_with_callback():
  pass