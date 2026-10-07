import pytest

from dictware import dig, every, has_value, some
from dictware import one


def test_nested_dict():
    assert dig({"a": {"b": {"c": 1}}}, "a", "b", "c") == 1

def test_mixed_dict_and_list():
    data = {"users": [{"name": "ann"}, {"name": "bob"}]}
    assert dig(data, "users", 1, "name") == "bob"
    assert dig(data, "users", -1, "name") == "bob"

def test_top_level_list():
    assert dig([[1, 2], [3, 4]], 1, 0) == 3

def test_missing_key_returns_none():
    assert dig({"a": {}}, "a", "b", "c") is None

def test_index_out_of_range_returns_none():
    assert dig({"a": [1]}, "a", 5) is None

def test_none_intermediate_returns_none():
    assert dig({"a": None}, "a", "b") is None

def test_no_keys_returns_obj():
    data = {"a": 1}
    assert dig(data) is data

def test_non_diggable_intermediate_raises():
    with pytest.raises(TypeError):
        dig({"a": 1}, "a", "b")

def test_list_with_string_key_raises():
    with pytest.raises(TypeError):
        dig({"a": [1, 2]}, "a", "0")

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
def test_every_no_callback(d, expected):
  assert(every(d) == expected)


def test_every_with_callback():
  l = {"a": 5, "b": 10}
  assert every(l) == True
  assert every(l, lambda k, v: k in ['a', 'b']) == True
  assert every(l, lambda k, v: v > 5) == False

@pytest.mark.parametrize(
  'd, expected',
  [
    [{}, False],
    [{"a": False, "b": []}, False],
    [{"a": False, "b": 0}, False],
    [{"a": False, "b": 2}, True]
  ]
)
def test_some_no_callback(d, expected):
  assert some(d) == expected

def test_any_with_callback():
  assert some({"a": 2, "b": 5}, lambda k, v: v > 5) == False
  assert some({"a": 2, "b": 5}, lambda k, v: v > 2) == True
@pytest.mark.parametrize(
  'd, expected',
  [
    [{}, False],
    [{"a": None}, False],
    [{"a": 1}, True],
    [{"a": 1, "b": None, "c": 0}, True],
    [{"a": 1, "b": "x"}, False],
    [{"a": [], "b": "", "c": False}, False],
  ]
)
def test_one_no_callback(d, expected):
  assert one(d) == expected

def test_one_with_callback():
  d = {"a": 2, "b": 5, "c": 8}
  assert one(d, lambda k, v: v > 6) == True
  assert one(d, lambda k, v: v > 3) == False
  assert one(d, lambda k, v: v > 10) == False
  assert one(d, lambda k, v: k == "b") == True

def test_one_callback_truthy_non_bool():
  assert one({"a": 0, "b": 5}, lambda k, v: v) == True
  assert one({"a": 3, "b": 5}, lambda k, v: v) == False

@pytest.mark.parametrize(
  'd, value, expected',
  [
    [{}, 1, False],
    [{"a": 1, "b": 2}, 2, True],
    [{"a": 1, "b": 2}, 3, False],
    [{"a": 1, "b": 2}, "a", False],
    [{"a": None}, None, True],
    [{"a": [1, 2]}, [1, 2], True],
    [{"a": {"x": 1}}, {"x": 1}, True],
  ]
)
def test_has_value(d, value, expected):
  assert has_value(d, value) == expected

def test_has_value_with_callback():
  d = {"a": 2, "b": 5}
  assert has_value(d, lambda k, v: v > 4) == True
  assert has_value(d, lambda k, v: v > 5) == False
  assert has_value(d, lambda k, v: k == "a" and v == 2) == True
  assert has_value({}, lambda k, v: True) == False

def test_has_value_callback_short_circuits():
  seen = []
  def cb(k, v):
    seen.append(k)
    return v == 1
  assert has_value({"a": 1, "b": 2}, cb) == True
  assert seen == ["a"]
