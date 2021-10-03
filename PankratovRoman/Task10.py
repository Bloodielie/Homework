from typing import Iterator


def endless_generator() -> Iterator[int]:
    number = 1
    while True:
        yield number
        number += 2


if __name__ == "__main__":
    gen = endless_generator()
    while True:
        print(next(gen))
