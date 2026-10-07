import re

import pytest

from dictware import (
    compact,
    delete_if,
    grep,
    grep_keys,
    grep_keys_v,
    grep_v,
    invert,
    reduce,
    reject,
    select,
    transform,
    transform_keys,
)


def test_transform_keys_empty_dict():
    assert transform_keys({}, lambda key, value: value ) == {}

def test_transform_keys_non_empty_dict():
    assert transform_keys({"a": 2}, lambda key, value: f"PRE_{key}_{value}") == {"PRE_a_2": 2}

def test_transform_keys_with_overwriting_keys():
    assert transform_keys({"pre_a": 2, "post_a": 5}, lambda key, value: "a") == {"a": 5}

def test_transform_keys_raises_error():
    with pytest.raises(TypeError):
        transform_keys({"pre_a": 2, "post_a": 5}, lambda key, value: {})

def test_transform_empty_dict():
    assert transform({}, lambda key, value: value ) == {}

def test_transform_non_empty_dict():
    assert transform({"a": 2, "b": 5}, lambda key, value: value * 2 ) == {"a": 4, "b": 10}

def test_reject_empty_dict():
    assert reject({}) == {}

def test_reject_non_empty_dict():
    assert reject({"a": "", "b": "foo"}) == {"a": ""}

def test_reject_with_cb():
    assert reject({"a": 2, "b": 5}, lambda key, value: value > 4) == {"a": 2}

def test_select_empty_dict():
    assert select({}) == {}

def test_select_with_falsy_keys():
    assert select({"a": "", "b": None}) == {}

def test_select_with_cb():
    assert select({"a": 5, "b": 2}, lambda key, value: value > 3) == { "a": 5 }

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


def test_compact_removes_none_by_default():
    assert compact({"a": 1, "b": None}) == {"a": 1}


def test_compact_keeps_other_falsy_values_by_default():
    data = {"a": 0, "b": False, "c": "", "d": [], "e": {}, "f": None}
    assert compact(data) == {"a": 0, "b": False, "c": "", "d": [], "e": {}}


def test_compact_only_none_false_removes_all_falsy_values():
    data = {"a": 0, "b": False, "c": "", "d": [], "e": {}, "f": None, "g": 1}
    assert compact(data, only_none=False) == {"g": 1}


def test_compact_is_shallow():
    assert compact({"a": {"b": None}}) == {"a": {"b": None}}


def test_compact_empty_dict():
    assert compact({}) == {}


def test_compact_does_not_mutate_input():
    data = {"a": None}
    compact(data)
    assert data == {"a": None}

def test_reduce_empty_dict():
    cb = lambda key, value, memo: memo
    assert reduce({}, cb, 0) == 0

def test_reduce_simple_sum():
    assert reduce({"a": 1, "b": 2}, lambda key, value, memo: memo + value, 0) == 3
    assert reduce({"a": 1, "b": 2}, lambda key, value, memo: memo + value, 10) == 13
def test_grep_empty_dict():
    assert grep({}, re.compile("foo")) == {}

def test_grep_matches_values():
    assert grep({"a": "foobar", "b": "bar", "c": "food"}, re.compile("foo")) == {"a": "foobar", "c": "food"}

def test_grep_matches_from_start_of_value():
    assert grep({"a": "foobar", "b": "barfoo"}, re.compile("foo")) == {"a": "foobar"}

def test_grep_converts_values_to_str():
    assert grep({"a": 10, "b": 25, "c": None}, re.compile(r"1\d")) == {"a": 10}

def test_grep_does_not_mutate_input():
    data = {"a": "foo", "b": "bar"}
    grep(data, re.compile("foo"))
    assert data == {"a": "foo", "b": "bar"}

def test_grep_v_empty_dict():
    assert grep_v({}, re.compile("foo")) == {}

def test_grep_v_rejects_matching_values():
    assert grep_v({"a": "foobar", "b": "barfoo", "c": 1}, re.compile("foo")) == {"b": "barfoo", "c": 1}

def test_grep_and_grep_v_partition_dict():
    data = {"a": "foo", "b": "bar", "c": 3}
    pattern = re.compile("foo")
    assert {**grep(data, pattern), **grep_v(data, pattern)} == data

def test_grep_keys_empty_dict():
    assert grep_keys({}, re.compile("user_")) == {}

def test_grep_keys_matches_keys():
    data = {"user_id": 1, "user_name": "bob", "age": 30}
    assert grep_keys(data, re.compile("user_")) == {"user_id": 1, "user_name": "bob"}

def test_grep_keys_converts_keys_to_str():
    assert grep_keys({1: "a", 10: "b", 2: "c"}, re.compile("1")) == {1: "a", 10: "b"}

def test_grep_keys_ignores_values():
    assert grep_keys({"a": "user_x"}, re.compile("user_")) == {}

def test_grep_keys_v_empty_dict():
    assert grep_keys_v({}, re.compile("user_")) == {}

def test_grep_keys_v_rejects_matching_keys():
    data = {"user_id": 1, "user_name": "bob", "age": 30}
    assert grep_keys_v(data, re.compile("user_")) == {"age": 30}

def test_grep_keys_and_grep_keys_v_partition_dict():
    data = {"user_id": 1, "age": 30, 5: "x"}
    pattern = re.compile("user_")
    assert {**grep_keys(data, pattern), **grep_keys_v(data, pattern)} == data

def test_delete_if_empty_dict():
    assert delete_if({}, lambda key, value: True) == {}

def test_delete_if_removes_matching_entries():
    assert delete_if({"a": 2, "b": 3, "c": 2}, lambda key, value: value == 2) == {"b": 3}

def test_delete_if_no_matches_leaves_dict_unchanged():
    assert delete_if({"a": 2, "b": 3}, lambda key, value: value > 10) == {"a": 2, "b": 3}

def test_delete_if_removes_all_entries():
    assert delete_if({"a": 2, "b": 3}, lambda key, value: True) == {}

def test_delete_if_uses_key_in_callback():
    assert delete_if({"tmp_a": 1, "b": 2}, lambda key, value: key.startswith("tmp_")) == {"b": 2}

def test_delete_if_treats_truthy_results_as_true():
    assert delete_if({"a": 0, "b": 5}, lambda key, value: value) == {"a": 0}

def test_delete_if_mutates_and_returns_same_dict():
    data = {"a": 2, "b": 3}
    result = delete_if(data, lambda key, value: value == 2)
    assert result is data
    assert data == {"b": 3}

def test_delete_if_calls_callback_once_per_entry():
    seen = []
    delete_if({"a": 1, "b": 2, "c": 3}, lambda key, value: seen.append((key, value)) or value != 2)
    assert seen == [("a", 1), ("b", 2), ("c", 3)]
