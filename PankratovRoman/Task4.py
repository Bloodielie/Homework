from typing import Sequence, Iterator


def split_by_indexes(string: str, indexes: Sequence[int]) -> Iterator[str]:
    temp = 0
    for index in indexes:
        yield string[temp: index]
        temp = index

    if temp < len(string):
        yield string[temp:]


if __name__ == '__main__':
    print(tuple(split_by_indexes("pythoniscool,isn'tit?", [6, 8, 12, 13, 18])))
    print(tuple(split_by_indexes("no luck", [42])))
