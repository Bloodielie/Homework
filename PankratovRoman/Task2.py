from contextlib import contextmanager
from typing import IO, Iterator


@contextmanager
def file_context_manager(filepath: str, mode: str = "r", encoding: str = "utf-8") -> Iterator[IO[str]]:
    file = open(filepath, mode, encoding=encoding)

    try:
        yield file
    except Exception as e:
        print(f"{e.__class__.__name__}: {e}")
        raise
    finally:
        file.close()


def main():
    with file_context_manager("../data/test_file.txt", "w") as input_file:
        print(input_file)


if __name__ == "__main__":
    main()
