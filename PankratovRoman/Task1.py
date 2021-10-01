from typing import Optional, IO


class FileContextManager:
    def __init__(self, filepath: str, mode: str = "r", encoding: str = "utf-8"):
        self._filepath = filepath
        self._mode = mode
        self._encoding = encoding
        self._file: Optional[IO[str]] = None

    def __enter__(self) -> IO[str]:
        try:
            file = open(self._filepath, self._mode, encoding=self._encoding)
            self._file = file
        except Exception as e:
            print(f"{e.__class__.__name__}: {e}")
            raise

        return file

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._file is not None:
            self._file.close()

        if exc_type:
            print(f"{exc_type}: {exc_val}\n")


def main():
    with FileContextManager("../data/test_file.txt", "w") as input_file:
        print(input_file)


if __name__ == "__main__":
    main()
