from typing import Iterator


def split(string: str, sep: str = " ") -> Iterator[str]:
    temp = 0
    for i, symbol in enumerate(string):
        if not symbol == sep:
            continue
        yield string[temp: i]
        temp = i + 1

    yield string[temp:]


if __name__ == '__main__':
    print(tuple(split("aaa,ddd,ccc", ",")))
    print(tuple(split("The most familiar palindromes in English")))
