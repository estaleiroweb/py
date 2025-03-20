import pytest
from ...core.fn import merge_recursive


def test_merge_recursive_dicts():
    """
    Tests the merge_recursive function with two dictionaries.

    Verifies that the function correctly merges two dictionaries, handling nested
    dictionaries and differing keys.
    """
    dict1 = {"a": 1, "b": {"x": 2, "y": 3}}
    dict2 = {"b": {"y": 4, "z": 5}, "c": 6}
    expected = {"a": 1, "b": {"x": 2, "y": 4, "z": 5}, "c": 6}
    assert merge_recursive(dict1, dict2) == expected


def test_merge_recursive_sets():
    """
    Tests the merge_recursive function with two sets.

    Verifies that the function correctly merges two sets, creating a union of the elements.
    """
    set1 = {1, 2, 3}
    set2 = {3, 4, 5}
    expected = {1, 2, 3, 4, 5}
    assert merge_recursive(set1, set2) == expected


def test_merge_recursive_lists():
    """
    Tests the merge_recursive function with two lists.

    Verifies that the function correctly merges two lists, concatenating them.
    """
    list1 = [1, 2, 3]
    list2 = [3, 4, 5]
    expected = [1, 2, 3, 3, 4, 5]
    assert merge_recursive(list1, list2) == expected


def test_merge_recursive_tuples():
    """
    Tests the merge_recursive function with two tuples.

    Verifies that the function correctly merges two tuples, concatenating them.
    """
    tuple1 = (1, 2, 3)
    tuple2 = (3, 4, 5)
    expected = (1, 2, 3, 3, 4, 5)
    assert merge_recursive(tuple1, tuple2) == expected


def test_merge_recursive_different_types():
    """
    Tests the merge_recursive function with different types.

    Verifies that the function correctly handles cases where the input values have
    different types, or when one of the values is None.
    """
    assert merge_recursive(1, "a") == "a"
    assert merge_recursive({"a": 1}, [1, 2]) == [1, 2]
    assert merge_recursive(None, 10) == 10


def test_merge_recursive_nested_dicts():
    """
    Tests the merge_recursive function with nested dictionaries.

    Verifies that the function correctly merges nested dictionaries, handling
    overlapping keys and differing levels of nesting.
    """
    dict1 = {"a": {"b": 1, "c": 2}, "d": 3}
    dict2 = {"a": {"c": 4, "e": 5}, "f": 6}
    expected = {"a": {"b": 1, "c": 4, "e": 5}, "d": 3, "f": 6}
    assert merge_recursive(dict1, dict2) == expected
