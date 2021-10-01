from contextlib import contextmanager
from time import perf_counter


@contextmanager
def time_execution_logger(filepath: str, encoding: str = "utf-8"):
    start = perf_counter()
    try:
        yield
    finally:
        with open(filepath, "a", encoding=encoding) as f:
            f.write(f"Execution time {(perf_counter()-start):.5f} sec\n")


@time_execution_logger("../data/time_execution_log.txt")
def test_func(first: int) -> None:
    for i in range(first):
        pass
    return None


def test2_func(first: int, second: int) -> None:
    return first ** second


def main():
    test_func(100000)

    with time_execution_logger("../data/time_execution_log.txt"):
        test2_func(100000, 2000)


if __name__ == "__main__":
    main()
