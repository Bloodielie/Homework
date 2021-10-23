"""Contains a content parser."""

from dataclasses import Field
from typing import Optional, List, Type, Dict, TypeVar, Any

from rss_parser.base import BaseTypeResolver, IParser, IContentWrapper
from rss_parser.exceptions import FindResolverError
from rss_parser.resolvers import (
    DataClassTypeResolver,
    StrTypeResolver,
    BoolTypeResolver,
    IntTypeResolver,
    ListTypeResolver,
    DatetimeTypeResolver,
    OptionalTypeResolver,
)

T = TypeVar("T", bound=Any)


class RSSParser(IParser):
    def __init__(self, type_resolvers: Optional[List[Type[BaseTypeResolver]]] = None):
        type_resolvers = type_resolvers or [
            DataClassTypeResolver,
            OptionalTypeResolver,
            StrTypeResolver,
            BoolTypeResolver,
            IntTypeResolver,
            ListTypeResolver,
            DatetimeTypeResolver,
        ]
        self._resolvers = [type_resolver(self) for type_resolver in type_resolvers]

    def parse_by_dataclass(self, content_wrapper: IContentWrapper, dataclass_: Type[T]) -> T:
        dict_schema = self.parse_by_schema(content_wrapper, dataclass_.__dataclass_fields__)
        return dataclass_(**dict_schema)

    def parse_by_schema(self, content_wrapper: IContentWrapper, schema: Dict[str, Field]) -> dict:
        args = {}
        for attr, field in schema.items():
            resolver = self.get_type_resolver(field.type)

            for tag_name in (*field.metadata.get("tag_names", []), attr):
                resolver_result = resolver.resolve(content_wrapper, tag_name, field.type)
                if isinstance(resolver_result, list) and len(resolver_result) == 0:
                    continue
                if resolver_result is not None:
                    break

            args[attr] = resolver_result

        return args

    def get_type_resolver(self, type_: Type[T]) -> BaseTypeResolver[T]:
        for type_resolver in self._resolvers:
            if type_resolver.check(type_):
                return type_resolver

        raise FindResolverError("Could not find a suitable resolver.")
