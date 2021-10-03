from typing import Iterator


def endless_fib_generator() -> Iterator[int]:
    previous, current = 0, 1
    while True:
        yield current
        previous, current = current, previous + current


if __name__ == "__main__":
    gen = endless_fib_generator()
    while True:
        print(next(gen))
