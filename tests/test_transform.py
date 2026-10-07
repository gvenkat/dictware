
from dictsy import compact, invert, reduce, select, reject, transform

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