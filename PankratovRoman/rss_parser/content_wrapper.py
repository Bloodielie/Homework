"""The module that includes classes for working with content."""

from collections.abc import Sequence
from typing import Optional, Union, Iterator, Any, Dict

from bs4 import BeautifulSoup, Tag

from rss_parser.base import IContentWrapper


class Bs4ContentWrapper(IContentWrapper):
    """Bs4 content wrapper

    Args:
        content: String to convert to tag or tag to find items.
    """

    def __init__(self, content: Union[str, Tag]):
        self._tag = content if isinstance(content, Tag) else BeautifulSoup(content, "xml")

    def find(self, key: str) -> Optional["Bs4ContentWrapper"]:
        """Finds nested tag by key and places it in a new instance of the Bs4ContentWrapper class.

        Args:
            key: Key for search nested Tag.

        Returns:
            Initialized Bs4ContentWrapper with tag found in content by key or None.
        """
        tag = self._tag.find(key)
        return Bs4ContentWrapper(tag) if tag is not None else None

    def find_all(self, key: str) -> Iterator["Bs4ContentWrapper"]:
        """Finds nested tag by key and places it in a new instance of the Bs4ContentWrapper class.

        Args:
            key: Key for search nested Tag.

        Yields:
            Initialized Bs4ContentWrapper with tag found in content by key.
        """
        for tag in self._tag.find_all(key):
            yield Bs4ContentWrapper(tag)

    def get(self, key: str) -> Optional[str]:
        """Gets attribute or text from Tag.

        Args:
            key: Key for get attribute or text.

        Returns:
            Attribute or None.
        """
        if key == "text":
            return getattr(self._tag, "text", None)
        return self._tag.get(key)

    def __str__(self) -> str:
        """Returns string representation of tag"""
        return str(self._tag)


class DictContentWrapper(IContentWrapper):
    """Dict content wrapper

    Args:
        content: Dict to find items.
    """

    def __init__(self, content: Dict[str, Any]):
        self._content = content

    def find(self, key: str) -> Optional["DictContentWrapper"]:
        """Finds nested dict by key and places it in a new instance of the DictContentWrapper class.

        Args:
            key: Key for search nested dict.

        Returns:
            Initialized DictContentWrapper with dict found in content by key or None.
        """
        value = self._content.get(key)
        return DictContentWrapper(value) if value is not None else None

    def find_all(self, key: str) -> Iterator["DictContentWrapper"]:
        """Finds nested dict by key and places it in a new instance of the DictContentWrapper class.

        Args:
            key: Key for search nested dict.

        Yields:
            Initialized DictContentWrapper with dict found in content by key.
        """
        value = self._content.get(key)
        if not isinstance(value, Sequence):
            return None

        for nested_value in value:
            yield DictContentWrapper(nested_value)

    def get(self, key: str) -> Optional[str]:
        """Gets field from dict.

        Args:
            key: Key for get field.

        Returns:
            Field string representation or None.
        """
        value = self._content.get(key)
        return str(value) if value is not None else None

    def __str__(self) -> str:
        """Returns string representation of dict"""
        return str(self._content)
