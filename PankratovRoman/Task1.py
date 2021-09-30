import sys


class Counter:
    def __init__(self, start: int = 0, stop: int = sys.maxsize):
        self._value = start
        self._stop = stop

    def increment(self) -> None:
        if self._value >= self._stop:
            raise ValueError("Maximal value is reached.")

        self._value += 1

    def get(self) -> int:
        return self._value


if __name__ == "__main__":
    first = Counter(start=42)
    first.increment()
    print(first.get())

    second = Counter()
    second.increment()
    print(second.get())
    second.increment()
    print(second.get())

    third = Counter(start=42, stop=43)
    third.increment()
    print(third.get())
    third.increment()
    print(third.get())
