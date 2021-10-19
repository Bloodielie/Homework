import pytest
from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper
from rss_parser.exceptions import FindResolverError, ResolveError
from rss_parser.parser import RSSParser
from rss_parser.resolvers import IntTypeResolver, StrTypeResolver
from rss_parser.schema import Rss


def test_parser(bs4_content_wrapper: Bs4ContentWrapper, dict_content_wrapper: DictContentWrapper):
    parser = RSSParser()

    assert isinstance(parser.get_type_resolver(str), StrTypeResolver)
    assert isinstance(parser.get_type_resolver(int), IntTypeResolver)

    with pytest.raises(FindResolverError):
        parser.get_type_resolver(set)

    assert isinstance(parser.parse_by_dataclass(bs4_content_wrapper.find("rss"), Rss), Rss)

    content_wrapper = Bs4ContentWrapper("<test>1</test>")
    with pytest.raises(ResolveError):
        assert isinstance(parser.parse_by_dataclass(content_wrapper, Rss), Rss)

    assert isinstance(parser.parse_by_dataclass(dict_content_wrapper, Rss), Rss)
