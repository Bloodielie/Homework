"""Module describing the interface of interaction with the main parts of the program."""

from abc import ABC, abstractmethod
from dataclasses import Field
from typing import Generic, Type, TypeVar, Any, Optional, Iterator, Dict

T = TypeVar("T", bound=Any)


class IParser(ABC):
    """Interface for Parser. Contains methods for parsing RSS channels"""

    @abstractmethod
    def parse_by_dataclass(self, content_wrapper: "IContentWrapper", dataclass_: Type[T]) -> T:
        """Parsing content in relation to the dataclass

        Args:
            content_wrapper: Object for working with content.
            dataclass_: Dataclass class describing the content schema for parsing.

        Returns:
            A dataclass instance with data.

        Raises:
            ResolveError: Data does not match the schema.
            FindResolverError: The schema contains a type that the parser does not know how to resolve.
        """

    @abstractmethod
    def parse_by_schema(self, content_wrapper: "IContentWrapper", schema: Dict[str, Field]) -> Dict[str, Any]:
        """Parsing content in relation to the schema

        Args:
            content_wrapper: Object for working with content.
            schema: Schema for parsing.

        Returns:
            A dictionary containing objects matching to the schema.

        Raises:
            ResolveError: Data does not match the schema.
            FindResolverError: The schema contains a type that the parser does not know how to resolve.
        """

    @abstractmethod
    def get_type_resolver(self, type_: Type[T]) -> "BaseTypeResolver[T]":
        """Search for a resolver matching to the type.

        Args:
            type_: The type matching to the resolver.

        Returns:
            The resolver matching to the type.

        Raises:
            FindResolverError: Could not find a resolver matching the type.
        """


class BaseTypeResolver(ABC, Generic[T]):
    """Base class for type resolver

    Args:
        parser: Parser object to recursively call parse_by_schema and get resolvers.
    """

    def __init__(self, parser: IParser):
        self._parser = parser

    @abstractmethod
    def check(self, type_: Type[T]) -> bool:
        """Checks recognizer for matching type.

        Args:
            type_: Type to check for compliance.

        Returns:
            If the type matches to the resolver returns true.
        """

    @abstractmethod
    def resolve(self, content_wrapper: "IContentWrapper", search_key: str, type_: Type[T]) -> T:
        """Resolves the type according to the content.

        Args:
            content_wrapper: Object for working with content.
            search_key: Key to search in content.
            type_: The type to which the content should be cast.

        Returns:
            Resolved type.

        Raises:
            ResolveError: Could not find or convert content to type.
        """


class IContentWrapper(ABC):
    """Interface for content wrapper class"""

    @abstractmethod
    def find(self, key: str) -> Optional["IContentWrapper"]:
        """Finds data nested within the content by key and places it in a new instance of the IContentWrapper class.

        Args:
            key: Key for search.

        Returns:
            Initialized IContentWrapper with data found in content by key or None.
        """

    @abstractmethod
    def find_all(self, key: str) -> Iterator["IContentWrapper"]:
        """Finds data nested within the content by key and places it in a new instance of the IContentWrapper class

        Args:
            key: Key for search.

        Yields:
            Initialized IContentWrapper with data found in content by key.
        """

    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        """Gets attribute from data.

        Args:
            key: Key for get attribute in data.

        Returns:
            Attribute or None.
        """

    @abstractmethod
    def __str__(self) -> str:
        """Returns the content nested in the wrapper"""
