from typing import Sequence


class MySquareIterator:
    def __init__(self, sequence: Sequence[int]):
        self._sequence = sequence
        self._iter_index = 0

    def __iter__(self) -> "MySquareIterator":
        self._iter_index = -1
        return self

    def __next__(self) -> int:
        self._iter_index += 1
        if self._iter_index >= len(self._sequence):
            raise StopIteration

        return self._sequence[self._iter_index] ** 2


if __name__ == "__main__":
    lst = [1, 2, 3, 4, 5]
    itr = MySquareIterator(lst)
    for item in itr:
        print(item)
