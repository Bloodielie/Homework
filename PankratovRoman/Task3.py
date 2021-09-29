from typing import Sequence, Iterator


def transform_to_sorted_unique_sequence(sequence: Sequence[str]) -> Sequence[str]:
    return sorted(set(sequence))


def get_divisors_iterator(number: int) -> Iterator[int]:
    return (i for i in range(1, number + 1) if not number % i)


def main():
    sequence = input("Enter comma separated sequence of words: ").split(",")
    print(transform_to_sorted_unique_sequence(sequence))

    number = int(input("Enter number: "))
    print(tuple(get_divisors_iterator(number)))


if __name__ == "__main__":
    main()
