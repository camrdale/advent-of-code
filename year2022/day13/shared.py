from typing import Any


def compare_nums(left: int, right: int) -> int:
    if left < right:
        return -1
    if right < left:
        return 1
    return 0


def compare_lists(left: list[Any], right: list[Any]) -> int:
    for left_element, right_element in zip(left, right):
        if type(left_element) == int and type(right_element) == int:
            order = compare_nums(left_element, right_element)
            if order != 0:
                return order
            continue

        if type(left_element) == int:
            left_element = [left_element]
        if type(right_element) == int:
            right_element = [right_element]
        assert type(left_element) == list
        assert type(right_element) == list

        order = compare_lists(left_element, right_element) # type: ignore
        if order != 0:
            return order

    return compare_nums(len(left), len(right))
