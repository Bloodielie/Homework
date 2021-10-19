from dataclasses import dataclass, is_dataclass
from datetime import datetime
from typing import List, Optional
from unittest.mock import Mock

import pytest
from rss_parser.content_wrapper import Bs4ContentWrapper
from rss_parser.exceptions import ResolveError
from rss_parser.resolvers import (
    BoolTypeResolver,
    DatetimeTypeResolver,
    IntTypeResolver,
    StrTypeResolver,
    DataClassTypeResolver,
    OptionalTypeResolver,
    ListTypeResolver,
)
from rss_parser.schema import Channel


def test_bool_resolver():
    mock = Mock()
    resolver = BoolTypeResolver(mock)

    assert resolver.check(bool)
    assert not resolver.check(str)
    assert not resolver.check(int)
    assert not resolver.check(List)

    content_wrapper = Bs4ContentWrapper("<test>true</test>")
    assert resolver.resolve(content_wrapper, "test", bool)

    assert isinstance(resolver.resolve(content_wrapper, "text", bool), bool)
    assert resolver.resolve(content_wrapper, "text", bool)

    content_wrapper = Bs4ContentWrapper("<test>false</test>")
    assert not resolver.resolve(content_wrapper, "test", bool)

    with pytest.raises(ResolveError):
        assert resolver.resolve(content_wrapper, "test_", bool)


def test_datetime_resolver():
    mock = Mock()
    resolver = DatetimeTypeResolver(mock)

    assert resolver.check(datetime)
    assert not resolver.check(str)
    assert not resolver.check(int)
    assert not resolver.check(List)

    content_wrapper = Bs4ContentWrapper("<test>Mon, 04 Oct 2021 09:51:11 -0400</test>")
    assert isinstance(resolver.resolve(content_wrapper, "test", datetime), datetime)
    assert isinstance(resolver.resolve(content_wrapper, "text", datetime), datetime)

    content_wrapper = Bs4ContentWrapper("<test>aaha</test>")
    with pytest.raises(ResolveError):
        assert isinstance(resolver.resolve(content_wrapper, "test", datetime), datetime)

    with pytest.raises(ResolveError):
        assert isinstance(resolver.resolve(content_wrapper, "test_", datetime), datetime)


def test_int_resolver():
    mock = Mock()
    resolver = IntTypeResolver(mock)

    assert resolver.check(int)
    assert not resolver.check(str)
    assert not resolver.check(set)
    assert not resolver.check(List)

    content_wrapper = Bs4ContentWrapper("<test>12</test>")
    assert isinstance(resolver.resolve(content_wrapper, "test", int), int)
    assert resolver.resolve(content_wrapper, "test", int) == 12

    assert isinstance(resolver.resolve(content_wrapper, "text", int), int)
    assert resolver.resolve(content_wrapper, "text", int) == 12

    content_wrapper = Bs4ContentWrapper("<test>aaha</test>")
    with pytest.raises(ResolveError):
        assert isinstance(resolver.resolve(content_wrapper, "test", int), int)

    with pytest.raises(ResolveError):
        assert isinstance(resolver.resolve(content_wrapper, "test_", int), int)


def test_str_resolver():
    mock = Mock()
    resolver = StrTypeResolver(mock)

    assert resolver.check(str)
    assert not resolver.check(int)
    assert not resolver.check(bool)
    assert not resolver.check(List)

    content_wrapper = Bs4ContentWrapper("<test>12</test>")
    assert isinstance(resolver.resolve(content_wrapper, "test", str), str)

    with pytest.raises(ResolveError):
        assert isinstance(resolver.resolve(content_wrapper, "test_", str), str)

    assert isinstance(resolver.resolve(content_wrapper, "text", str), str)
    assert resolver.resolve(content_wrapper, "text", str) == "12"


def test_dataclass_resolver():
    mock = Mock()
    resolver = DataClassTypeResolver(mock)

    assert resolver.check(Channel)
    assert not resolver.check(int)
    assert not resolver.check(bool)
    assert not resolver.check(List)

    @dataclass
    class Test:
        title: int

    mock = Mock()
    mock.parse_by_schema.return_value = {"title": 1}
    resolver = DataClassTypeResolver(mock)

    content_wrapper = Bs4ContentWrapper("<test><title>1</title></test>")
    result = resolver.resolve(content_wrapper, "test", Test)

    assert is_dataclass(result)
    assert isinstance(result, Test)
    assert isinstance(result.title, int)

    assert resolver.resolve(content_wrapper, "test_", Test) is None


def test_optional_resolver():
    mock = Mock()
    resolver = OptionalTypeResolver(mock)

    assert resolver.check(Optional[str])
    assert not resolver.check(int)
    assert not resolver.check(bool)
    assert not resolver.check(List)

    mock = Mock()
    mock.get_type_resolver.return_value = StrTypeResolver(Mock())
    resolver = OptionalTypeResolver(mock)

    content_wrapper = Bs4ContentWrapper("<test>nice</test>")
    assert isinstance(resolver.resolve(content_wrapper, "test", Optional[str]), str)
    assert resolver.resolve(content_wrapper, "test_", Optional[str]) is None


def test_list_resolver():
    mock = Mock()
    resolver = ListTypeResolver(mock)

    assert resolver.check(List[str])
    assert not resolver.check(int)
    assert not resolver.check(bool)
    assert not resolver.check(set)

    @dataclass
    class Test:
        title: int

    mock = Mock()
    mock.parse_by_schema.return_value = {"title": 1}
    resolver = ListTypeResolver(mock)

    content_wrapper = Bs4ContentWrapper("<test2><test><title>1</title></test><test><title>2</title></test></test2>")
    result = resolver.resolve(content_wrapper, "test", List[Test])
    assert isinstance(result, list)
    for test in result:
        assert isinstance(test, Test)

    result2 = resolver.resolve(content_wrapper, "test_", List[Test])
    assert isinstance(result, list)
    assert len(result2) == 0
