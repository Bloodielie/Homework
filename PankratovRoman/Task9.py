from typing import Union


class EvenRange:
    def __init__(self, start: int, stop: int):
        self._start = start
        self._stop = stop

        self._first_even_number = start if (start % 2) == 0 else start + 1
        self._last_even_number = stop - 2 if (stop % 2) == 0 else stop - 1

        self._current_even_number = self._first_even_number - 2

    def __iter__(self) -> "EvenRange":
        self._current_even_number = self._first_even_number - 2
        return self

    def __next__(self) -> Union[int, str]:
        self._current_even_number += 2
        if self._current_even_number > self._last_even_number:
            return "Out of numbers!"

        return self._current_even_number


if __name__ == "__main__":
    er1 = EvenRange(7, 11)
    print(next(er1))
    print(next(er1))
    print(next(er1))
    print(next(er1))

    for number in er1:
        print(number)
        if isinstance(number, str):
            break

    er2 = EvenRange(3, 14)
    for number in er2:
        print(number)
        if isinstance(number, str):
            break
