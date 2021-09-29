from typing import TypeVar, Dict

K = TypeVar("K")
V = TypeVar("V")


def sort_dict_by_key(unsorted_dict: Dict[K, V]) -> Dict[K, V]:
    return dict(sorted(unsorted_dict.items()))


if __name__ == "__main__":
    example_dict_one = {1: "test", 3: "test3", 8: "test8", 5: "test5", 2: "test2"}
    print(sort_dict_by_key(example_dict_one))
