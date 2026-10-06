import pytest

from dictsy import all, any

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
  l = {"a": 5, "b": 10}
  assert all(l) == True
  assert all(l, lambda k, v: k in ['a', 'b']) == True
  assert all(l, lambda k, v: v > 5) == False

@pytest.mark.parametrize(
  'd, expected',
  [
    [{}, False],
    [{"a": False, "b": []}, False],
    [{"a": False, "b": 0}, False],
    [{"a": False, "b": 2}, True]
  ]
)
def test_any_no_callback(d, expected):
  assert any(d) == expected

def test_any_with_callback():
  assert any({"a": 2, "b": 5}, lambda k, v: v > 5) == False
  assert any({"a": 2, "b": 5}, lambda k, v: v > 2) == True