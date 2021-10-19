from dataclasses import dataclass
from datetime import datetime

from rss_parser.converter import get_dict, get_text
from rss_parser.schema import Channel


def test_get_dict():
    @dataclass
    class Test:
        test1: str
        test2: int
        date: datetime

    test_dataclass = Test(test1="test", test2=1, date=datetime(2005, 7, 14))
    dict_representation = get_dict(test_dataclass)
    assert isinstance(dict_representation, dict)
    assert dict_representation == {"test1": "test", "test2": 1, "date": "2005-07-14 00:00:00"}


def test_get_text():
    channel = Channel(
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
