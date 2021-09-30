from collections import defaultdict
from typing import Dict, DefaultDict


def combine_dicts(*args: Dict[str, int]) -> Dict[str, int]:
    result: DefaultDict[str, int] = defaultdict(int)
    for dict_ in args:
        for key, value in dict_.items():
            result[key] += value
    return result


if __name__ == "__main__":
    dict_1 = {"a": 100, "b": 200}
    dict_2 = {"a": 200, "c": 300}
    dict_3 = {"a": 300, "d": 100}

    print(combine_dicts(dict_1, dict_2))
    print(combine_dicts(dict_1, dict_2, dict_3))
