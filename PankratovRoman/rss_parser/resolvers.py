"""Contains resolvers for different types."""

from dataclasses import is_dataclass
from datetime import datetime
from typing import Optional, List, Type, TypeVar, Any

from dateutil import parser
from dateutil.parser import ParserError

from rss_parser.base import BaseTypeResolver, IContentWrapper
from rss_parser.exceptions import ResolveError
from rss_parser.types import DataClassType
from rss_parser.utils import is_optional_typing, is_list_typing

T = TypeVar("T", bound=Any)


def _find_element_in_content(content_wrapper: IContentWrapper, search_key: str) -> str:
    """Searches element in the content.

    Args:
        content_wrapper: Object for working with content.
        search_key: Key to find an item in content.

    Return:
        Found element.

    Raise:
        ResolveError: Could not find element.
    """
    value = content_wrapper.get(search_key)
    if value is None:
        nested_content_wrapper = content_wrapper.find(search_key)
        if nested_content_wrapper is not None:
            value = nested_content_wrapper.get("text")

    if value is None:
        raise ResolveError(f"Could not find {search_key} element in {content_wrapper}")

    return value


class DataClassTypeResolver(BaseTypeResolver[DataClassType]):
    def check(self, type_: Type[DataClassType]) -> bool:
        return is_dataclass(type_)

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[DataClassType]) -> DataClassType:
        new_tag = content_wrapper.find(search_key)
        if new_tag is None:
            return None

        dataclass_args = self._parser.parse_by_schema(new_tag, type_.__dataclass_fields__)
        dataclass_ = type_(**dataclass_args)
        return dataclass_


class OptionalTypeResolver(BaseTypeResolver[Optional[T]]):
    def check(self, type_: Type[Optional[T]]) -> bool:
        return is_optional_typing(type_)

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[Optional[T]]) -> Optional[T]:
        type_ = type_.__args__[0]  # type: ignore
        resolver = self._parser.get_type_resolver(type_)
        try:
            return resolver.resolve(content_wrapper, search_key, type_)
        except ResolveError:
            return None


class ListTypeResolver(BaseTypeResolver[List[T]]):
    def check(self, type_: Type[List[T]]) -> bool:
        return is_list_typing(type_)

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[List[T]]) -> List[T]:
        inner_type = type_.__args__[0]  # type: ignore

        elements = []
        for nested_tag in content_wrapper.find_all(search_key):
            schema = self._parser.parse_by_schema(nested_tag, inner_type.__dataclass_fields__)
            elements.append(inner_type(**schema))
        return elements


class StrTypeResolver(BaseTypeResolver[str]):
    def check(self, type_: Type[str]) -> bool:
        try:
            return issubclass(type_, str)
        except TypeError:
            return False

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[str]) -> str:
        return _find_element_in_content(content_wrapper, search_key)


class IntTypeResolver(BaseTypeResolver[int]):
    def check(self, type_: Type[int]) -> bool:
        try:
            return issubclass(type_, int)
        except TypeError:
            return False

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[int]) -> int:
        try:
            return int(_find_element_in_content(content_wrapper, search_key))
        except ValueError:
            raise ResolveError(f"The type of {search_key} tag found does not match int")


class DatetimeTypeResolver(BaseTypeResolver[datetime]):
    def check(self, type_: Type[datetime]) -> bool:
        try:
            return issubclass(type_, datetime)
        except TypeError:
            return False

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[datetime]) -> datetime:
        value = _find_element_in_content(content_wrapper, search_key)
        try:
            return parser.parse(value)
        except ParserError:
            raise ResolveError(f"The type of {search_key} tag found does not match datetime")


class BoolTypeResolver(BaseTypeResolver[bool]):
    def check(self, type_: Type[bool]) -> bool:
        return type_ is bool

    def resolve(self, content_wrapper: IContentWrapper, search_key: str, type_: Type[bool]) -> bool:
        value = _find_element_in_content(content_wrapper, search_key)
        return True if value == "true" else False
