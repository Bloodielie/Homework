import argparse
import logging
from dataclasses import dataclass
from typing import Optional, List, Union, Tuple

from rss_parser.utils import is_optional_typing, is_list_typing, is_valid_url, init_argparse, get_console_handler, \
    convert_namespace_to_dataclass


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


def test_init_argparse():
    parser = init_argparse()

    assert isinstance(parser, argparse.ArgumentParser)

    args = parser.parse_args(["https://test.by/"])
    assert args.source is not None
    assert isinstance(args.source, str)
    assert args.source == "https://test.by/"

    args = parser.parse_args(["--limit", "5", "--date", "20211202", "https://test.by/"])
    assert args.limit is not None
    assert isinstance(args.limit, int)
    assert args.limit == 5

    assert args.date is not None
    assert isinstance(args.date, str)
    assert args.date == "20211202"

    assert args.json is not None
    assert isinstance(args.json, bool)
    assert not args.json

    args = parser.parse_args(["--json", "https://test.by/"])
    assert args.json is not None
    assert isinstance(args.json, bool)
    assert args.json


def test_get_console_handler():
    console_handler = get_console_handler(False, False)
    assert console_handler.level is logging.INFO

    console_handler = get_console_handler(True, False)
    assert console_handler.level is logging.DEBUG


def test_convert_namespace_to_dataclass():
    @dataclass
    class Test:
        a: str
        b: int

    init_dataclass = convert_namespace_to_dataclass(argparse.Namespace(a="1", b=1), Test)

    assert isinstance(init_dataclass, Test)

    assert isinstance(init_dataclass.a, str)
    assert init_dataclass.a == "1"

    assert isinstance(init_dataclass.b, int)
    assert init_dataclass.b == 1
