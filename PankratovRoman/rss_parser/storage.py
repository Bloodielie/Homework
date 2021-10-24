"""Contains classes for working with various data stores."""

import json

from rss_parser.base import BaseStorage


class FileStorage(BaseStorage):
    """Сlass for working with data in the file.

    Args:
        file_path: Path to file for working.
        encoding: Working file encoding.
    """

    def __init__(self, file_path: str, encoding: str = "utf-8"):
        open(file_path, "a").close()
        self._file = open(file_path, "r+", encoding=encoding)

        data_from_file = self._file.read()
        data = json.loads(data_from_file) if data_from_file else {}
        super().__init__(data)

    def save(self) -> None:
        """Saves data to open file"""
        self._file.seek(0)
        self._file.write(json.dumps(self.data, default=str))

    def close(self) -> None:
        """Closes working file"""
        self._file.close()
