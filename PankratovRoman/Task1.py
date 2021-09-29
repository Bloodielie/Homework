def str_len(string: str) -> int:
    if not string:
        return 0
    return sum(1 for _ in string)


if __name__ == "__main__":
    assert str_len("Hello world") == len("Hello world")
    assert str_len("Hi") == len("Hi")
    assert str_len("") == len("")
