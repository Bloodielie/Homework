from typing import Sequence, Iterator


def foo(sequence: Sequence[int]) -> Iterator[int]:
    for i in range(len(sequence)):
        temp = 1
        for j, number in enumerate(sequence):
            if i == j:
                continue
            temp *= number
        yield temp


if __name__ == "__main__":
    print(tuple(foo([1, 2, 3, 4, 5])))
    print(tuple(foo([3, 2, 1])))
