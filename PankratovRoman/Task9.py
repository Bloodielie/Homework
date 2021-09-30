from string import ascii_lowercase
from typing import Set


def test_1_1(*args: str) -> Set[str]:
    result = set(args[0])
    for string in args[1:]:
        result &= set(string)
    return result


def test_1_2(*args: str) -> Set[str]:
    return {element for string in args for element in string}


def test_1_3(*args: str) -> Set[str]:
    result = set()
    first_element_set = set(args[0])
    for string in args[1:]:
        result.update(first_element_set & set(string))
    return result


def test_1_4(*args: str) -> Set[str]:
    set_result = set(ascii_lowercase)
    for elem in args:
        set_result -= set(elem)
    return set_result


if __name__ == "__main__":
    test_strings = [
        "hello",
        "world",
        "python",
    ]
    print(test_1_1(*test_strings))
    print(test_1_2(*test_strings))
    print(test_1_3(*test_strings))
    print(test_1_4(*test_strings))
