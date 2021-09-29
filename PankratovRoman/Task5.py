from typing import Sequence, Set, TypeVar, Dict

K = TypeVar("K")
V = TypeVar("V")


def get_unique_values(dict_sequence: Sequence[Dict[K, V]]) -> Set[V]:
    return {tuple(dict_.values())[0] for dict_ in dict_sequence}


if __name__ == "__main__":
    example_list = [
        {"V": "S001"},
        {"V": "S002"},
        {"VI": "S001"},
        {"VI": "S005"},
        {"VII": "S005"},
        {"V": "S009"},
        {"VIII": "S007"},
    ]
    print(get_unique_values(example_list))
