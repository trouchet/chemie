import pytest
from functools import reduce
from backend.app.api.utils.native import (
    invert_dict,
    flatten_list,
    sum_dicts,
    remove_list_from_list,
    get_random_element,
    setify_list,
    remove_duplicates_and_select_max,
    generate_random_tokens,
)

def test_remove_duplicates_and_select_max_empty_list():
    """Test remove_duplicates_and_select_max with an empty list."""
    empty_list = []
    result = remove_duplicates_and_select_max(empty_list)
    assert result == []


def test_remove_duplicates_and_select_max_single_element():
    """Test remove_duplicates_and_select_max with a list containing a single element."""
    single_element_list = [("key", 10)]
    result = remove_duplicates_and_select_max(single_element_list)
    assert result == [("key", 10)]


def test_remove_duplicates_and_select_max_multiple_elements():
    """Test remove_duplicates_and_select_max with a list containing duplicates and selecting the max."""
    data = [("key1", 5), ("key2", 3), ("key1", 8), ("key3", 1)]
    result = remove_duplicates_and_select_max(data)
    assert result == [("key1", 8), ("key2", 3), ("key3", 1)]


def test_generate_random_tokens():
    
    token_length = 5
    tokens = generate_random_tokens(2, token_length)
    result = reduce(
        lambda a, b: a and b,
        map(lambda x: x == token_length, map(len, tokens)),
        True
    )
    assert result is True

def test_setify_list_empty_list():
    """Test setify_list with an empty list."""
    empty_list = []
    result = setify_list(empty_list)
    assert result == []


def test_setify_list_no_duplicates():
    """Test setify_list with a list containing no duplicates."""
    unique_list = ["apple", "banana", "orange"]
    result = setify_list(unique_list)
    assert set(result) == set(["apple", "banana", "orange"])


def test_setify_list_with_duplicates():
    """Test setify_list with a list containing duplicates."""
    list_with_duplicates = ["apple", "banana", "apple", "orange"]
    result = setify_list(list_with_duplicates)
    assert set(result) == set(["apple", "banana", "orange"])  # Order may vary


def test_remove_list_from_list_empty_list1():
    """Test remove_list_from_list with an empty list1."""
    list1 = []
    list2 = [1, 2, 3]
    result = remove_list_from_list(list1, list2)
    assert result == []


def test_remove_list_from_list_empty_list2():
    """Test remove_list_from_list with an empty list2."""
    list1 = [1, 2, 3]
    list2 = []
    result = remove_list_from_list(list1, list2)
    assert result == [1, 2, 3]


def test_remove_list_from_list_no_overlap():
    """Test remove_list_from_list with no overlap between lists."""
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    result = remove_list_from_list(list1, list2)
    assert result == [1, 2, 3]


def test_remove_list_from_list_with_overlap():
    """Test remove_list_from_list with elements present in both lists."""
    list1 = [1, 2, 3, 4]
    list2 = [2, 4, 5]
    result = remove_list_from_list(list1, list2)
    assert result == [1, 3]


def test_get_random_element_empty_list():
    """Test get_random_element with an empty list."""
    with pytest.raises(ValueError):
        get_random_element([])


def test_get_random_element_single_element():
    """Test get_random_element with a list containing a single element."""
    single_element = [10]
    result = get_random_element(single_element)
    assert result == 10


def test_invert_dict_failed(mangled_sample_dict):
    with pytest.raises(ValueError) as e:
        invert_dict(mangled_sample_dict)

    assert str(e.value) == "All values must be lists!"


def test_invert_dict(sample_dict):
    inverted_dict = invert_dict(sample_dict)
    assert inverted_dict == {
        1: ["a"],
        2: ["a", "b"],
        3: ["a", "c"],
        4: ["b"],
        6: ["b", "c"],
        9: ["c"],
    }


def test_flatten_list():
    lst = [[1, 2], [3, [4, 5]], 6]
    assert flatten_list(lst) == [1, 2, 3, 4, 5, 6]


def test_sum_dicts():
    dict_list = [{"a": 1, "b": 2}, {"b": 3, "c": 4}, {"c": 5, "d": 6}]
    assert sum_dicts(dict_list) == {"a": 1, "b": 5, "c": 9, "d": 6}


@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([1, 2, 3, 4, 5], [2, 4], [1, 3, 5]),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], []),
        ([1, 2, 3, 4, 5], [], [1, 2, 3, 4, 5]),
        ([], [1, 2, 3, 4, 5], []),
        ([], [], []),
    ],
)
def test_remove_list_from_list(list1, list2, expected):
    assert remove_list_from_list(list1, list2) == expected


def test_remove_list_from_list_handles_duplicates():
    list1 = [1, 2, 2, 3, 4, 5]
    list2 = [2, 4]
    expected = [1, 3, 5]
    assert remove_list_from_list(list1, list2) == expected


def test_remove_list_from_list_returns_new_list():
    list1 = [1, 2, 3, 4, 5]
    list2 = [2, 4]
    result = remove_list_from_list(list1, list2)
    assert result is not list1
    assert result is not list2
