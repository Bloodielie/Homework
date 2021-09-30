from typing import Dict


def generate_squares(number: int) -> Dict[int, int]:
    return {i: i * i for i in range(1, number + 1)}


if __name__ == "__main__":
    print(generate_squares(5))
