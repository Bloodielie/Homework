from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper


def test_bs4_content_wrapper(bs4_content_wrapper: Bs4ContentWrapper):
    rss = bs4_content_wrapper.find("rss")
    assert isinstance(rss, Bs4ContentWrapper)
    assert bs4_content_wrapper.find("Test") is None

    assert isinstance(rss.get("version"), str)
    assert rss.get("version") == "2.0"

    channel = rss.find("channel")
    channel_title = channel.find("title")
    channel_title_text = channel_title.get("text")

    assert isinstance(str(channel_title), str)
    assert str(channel_title) == "<title>Yahoo News</title>"

    assert isinstance(channel_title_text, str)
    assert channel_title_text == "Yahoo News"

    items = list(channel.find_all("item"))

    assert isinstance(items, list)
    assert len(items) == 2


def test_dict_content_wrapper(dict_content_wrapper: DictContentWrapper):
    assert isinstance(dict_content_wrapper.get("version"), str)
    assert dict_content_wrapper.find("Test") is None

    assert isinstance(dict_content_wrapper.get("version"), str)
    assert dict_content_wrapper.get("version") == "2.0"

    channel = dict_content_wrapper.find("channel")
    channel_title = channel.get("title")

    assert channel.get("Test") is None

    assert isinstance(channel_title, str)
    assert channel_title == "Yahoo News"

    assert isinstance(str(channel_title), str)

    items = list(channel.find_all("items"))
    assert isinstance(items, list)
    assert len(items) == 2

    for item in items:
        assert isinstance(item.find("guid").get("text"), str)

    assert isinstance(str(dict_content_wrapper), str)
