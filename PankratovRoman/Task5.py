from typing import Tuple


def get_digits(num: int) -> Tuple[int, ...]:
    return tuple(int(digit) for digit in str(num))


if __name__ == "__main__":
    print(get_digits(87178291199))
