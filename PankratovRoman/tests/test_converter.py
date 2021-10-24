from dataclasses import dataclass
from datetime import datetime

import pytest

from rss_parser.converter import get_json_text, get_text, get_html_text
from rss_parser.schema import Channel


@pytest.fixture()
def channel():
    return Channel(
        title="Test",
        link="Link",
        description="Description",
        pub_date=datetime(2005, 7, 14),
        language=None,
        copyright=None,
        managing_editor=None,
        web_master=None,
        last_build_date=None,
        category=None,
        generator=None,
        docs=None,
        ttl=None,
        image=None,
        cloud=None,
        text_input=None,
        rating=None,
        items=[]
    )


def test_get_dict():
    @dataclass
    class Test:
        test1: str
        test2: int
        date: datetime

    test_dataclass = Test(test1="test", test2=1, date=datetime(2005, 7, 14))
    dict_representation = get_json_text(test_dataclass)
    assert isinstance(dict_representation, str)
    assert dict_representation == '{\n    "test1": "test",\n    "test2": 1,\n    "date": "2005-07-14 00:00:00"\n}'


def test_get_text(channel: Channel):
    result = """Channel:
    Title: Test
    Description: Description
    Date: 2005-07-14 00:00:00
    Link: Link
    Image: None

Items:"""

    text_representation = get_text(channel)

    assert isinstance(text_representation, str)
    assert text_representation == result


def test_get_html(channel: Channel):
    html = get_html_text([channel])

    assert isinstance(html, str)
