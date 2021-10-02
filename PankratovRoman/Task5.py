class NumberException(Exception):
    pass


class NumberTooSmall(NumberException):
    pass


class NumberIsNotEven(NumberException):
    pass


def is_even(number: int) -> bool:
    if number <= 2:
        raise NumberTooSmall("The number is too small.")
    even = number % 2 == 0
    if not even:
        raise NumberIsNotEven("The number is not even.")
    return even


if __name__ == "__main__":
    print(is_even(4))

    try:
        print(is_even(0))
    except NumberException as e:
        print(f"{e.__class__.__name__}: {e}")

    try:
        print(is_even(3))
    except NumberException as e:
        print(f"{e.__class__.__name__}: {e}")
