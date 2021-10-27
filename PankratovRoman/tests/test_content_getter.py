from collections.abc import Sequence
from unittest.mock import Mock

from rss_parser.content_getter import InternetContentGetter, StorageContentGetter
from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper


def test_storage_content_getter():
    console_args = Mock()

    storage = Mock()
    storage.get.return_value = None

    content_getter = StorageContentGetter(storage)
    content_wrappers = content_getter.get_content_wrappers(console_args)
    assert content_wrappers is None

    console_args.source = "test"

    storage.get.return_value = {}
    content_wrappers = content_getter.get_content_wrappers(console_args)
    assert content_wrappers is None

    storage.get.return_value = {"test": [{"name": "ilya"}]}
    content_wrappers = content_getter.get_content_wrappers(console_args)
    assert isinstance(content_wrappers, Sequence)
    assert isinstance(content_wrappers[0], DictContentWrapper)

    console_args.source = None
    content_wrappers = content_getter.get_content_wrappers(console_args)
    assert isinstance(content_wrappers, Sequence)
    assert isinstance(content_wrappers[0], DictContentWrapper)


def test_internet_content_getter(mocker):
    response = Mock(ok=False)

    def feick_get(*args, **kwargs):
        return response
    mocker.patch("requests.get", feick_get)

    content_getter = InternetContentGetter()
    console_args = Mock()
    console_args.source = "test"

    content_wrapper = content_getter.get_content_wrappers(console_args)
    assert content_wrapper is None

    response = Mock(ok=True, text="")

    content_wrapper = content_getter.get_content_wrappers(console_args)
    assert content_wrapper is None

    response = Mock(ok=True, text="<channel><title>Nice</title></channel>")

    content_wrapper = content_getter.get_content_wrappers(console_args)
    assert isinstance(content_wrapper, Sequence)
    assert isinstance(content_wrapper[0], Bs4ContentWrapper)
