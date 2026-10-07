import pytest

from dictsy import dig, every, some


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