from typing import Optional, List, Union, Tuple

from rss_parser.utils import is_optional_typing, is_list_typing, is_valid_url


def test_optional_typing():
    assert is_optional_typing(Optional[str])
    assert is_optional_typing(Optional[int])
    assert is_optional_typing(Union[int, None])

    assert not is_optional_typing(Union[int, str])
    assert not is_optional_typing(str)
    assert not is_optional_typing(int)
    assert not is_optional_typing(List[int])


def test_list_typing():
    assert is_list_typing(List[str])
    assert is_list_typing(List[int])

    assert not is_list_typing(str)
    assert not is_list_typing(int)

    assert not is_list_typing(Tuple[str])
    assert not is_list_typing(Tuple[int])


def test_is_valid_url():
    assert is_valid_url("https://github.com/")
    assert is_valid_url("http://www.twitch.tv/")

    assert not is_valid_url("github.com")
    assert not is_valid_url("www.twitch")
    assert not is_valid_url("https://test[.com")
