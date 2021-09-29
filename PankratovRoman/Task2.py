from collections import defaultdict
from typing import Dict, DefaultDict


def count_chars(string: str) -> Dict[str, int]:
    frequency: DefaultDict[str, int] = defaultdict(int)
    for letter in string:
        frequency[letter] += 1
    return frequency


if __name__ == "__main__":
    print(count_chars("Hello world"))
    print(count_chars("Very well"))
    print(count_chars("ABCD DCBA"))
