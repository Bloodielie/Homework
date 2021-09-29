from typing import Sequence


def convert_int_sequence_to_int(sequence: Sequence[int]) -> int:
    return int("".join(map(str, sequence)))


def print_multiplication_table(a: int, b: int, c: int, d: int) -> None:
    print("\t", "\t".join(map(str, range(c, d + 1))), sep="")
    for row in range(a, b + 1):
        print(row, end="\t")
        for column in range(c, d + 1):
            print(row * column, end="\t")
        print()


if __name__ == "__main__":
    example_tuple = (1, 2, 3, 4)
    result = convert_int_sequence_to_int(example_tuple)
    print(f"Result: {result}, Result type: {type(result)}")

    a, b, c, d = 2, 4, 3, 7
    print_multiplication_table(a, b, c, d)
