import pytest

from dictsy.utils import dig, invert


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


def test_invert_swaps_keys_and_values():
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_invert_skips_unhashable_values():
    assert invert({"a": 1, "b": [2], "c": {"x": 3}, "d": (1, [2])}) == {1: "a"}


def test_invert_duplicate_values_last_wins():
    assert invert({"a": 1, "b": 1}) == {1: "b"}


def test_invert_does_not_mutate_input():
    data = {"a": 1}
    invert(data)
    assert data == {"a": 1}
