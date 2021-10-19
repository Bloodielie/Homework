from datetime import datetime

import pytest
from dateutil.tz import tzoffset, tzutc
from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper


@pytest.fixture(scope="session")
def bs4_content_wrapper() -> Bs4ContentWrapper:
    rss = """
    <rss version="2.0">
    <channel>
        <title>Yahoo News</title>
        <link>https://www.yahoo.com/news</link>
        <description>The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.</description>
        <language>en-US</language>
        <copyright>Copyright (c) 2021 Yahoo! Inc. All rights reserved</copyright>
        <pubDate>Mon, 04 Oct 2021 09:51:11 -0400</pubDate>
        <ttl>5</ttl>
        <image>
            <title>Yahoo News - Latest News &amp; Headlines</title>
            <link>https://www.yahoo.com/news</link>
            <url>http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png</url>
        </image>
        <item>
            <title>No winner: Biggest Powerball jackpot in months grows larger</title>
            <link>https://news.yahoo.com/powerball-jackpot-biggest-lottery-prize-142243642.html</link>
            <pubDate>2021-10-02T14:22:43Z</pubDate>
            <source url="http://www.ap.org/">Associated Press</source>
            <guid isPermaLink="false">powerball-jackpot-biggest-lottery-prize-142243642.html</guid>
            <media:content height="86" url="https://s.yimg.com/uu/api/res/1.2" width="130" />
            <media:credit role="publishing company" />
        </item>
        <item>
            <title>Jerry Seinfeld apologizes for the 'uncomfortable subtle sexual aspect' between a human and an insect in 'Bee Movie'</title>
            <link>https://news.yahoo.com/jerry-seinfeld-apologizes-uncomfortable-subtle-203443120.html</link>
            <pubDate>2021-10-03T20:34:43Z</pubDate>
            <source url="https://www.insider.com/">INSIDER</source>
            <guid isPermaLink="false">jerry-seinfeld-apologizes-uncomfortable-subtle-203443120.html</guid>
            <media:content height="86" url="https://s.yimg.com/uu/api/res/1.2/soiykgrPVcKzGRcrhaa" width="130" />
            <media:credit role="publishing company" />
        </item>
    </channel>
    </rss>
    """

    return Bs4ContentWrapper(rss)


@pytest.fixture(scope="session")
def dict_content_wrapper():
    rss_dict = {
        "version": "2.0",
        "channel": {
            "title": "Yahoo News",
            "link": "https://www.yahoo.com/news",
            "description": "The latest news and headlines from Yahoo! News. Get breaking news stories and in-depth coverage with videos and photos.",
            "language": "en-US",
            "copyright": "Copyright (c) 2021 Yahoo! Inc. All rights reserved",
            "managing_editor": None,
            "web_master": None,
            "pub_date": datetime(2021, 10, 4, 9, 51, 11, tzinfo=tzoffset(None, -14400)),
            "last_build_date": None,
            "category": None,
            "generator": None,
            "docs": None,
            "ttl": 5,
            "image": {
                "title": "Yahoo News - Latest News  Headlines",
                "link": "https://www.yahoo.com/news",
                "url": "http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png",
                "description": None,
                "width": None,
                "height": None,
            },
            "cloud": None,
            "rating": None,
            "text_input": None,
            "items": [
                {
                    "title": "No winner: Biggest Powerball jackpot in months grows larger",
                    "link": "https://news.yahoo.com/powerball-jackpot-biggest-lottery-prize-142243642.html",
                    "description": None,
                    "author": None,
                    "category": None,
                    "comments": None,
                    "enclosure": None,
                    "guid": {"is_perm_link": False, "text": "powerball-jackpot-biggest-lottery-prize-142243642.html"},
                    "pub_date": datetime(2021, 10, 2, 14, 22, 43, tzinfo=tzutc()),
                    "source": {"url": "http://www.ap.org/", "text": "Associated Press"},
                },
                {
                    "title": "Jerry Seinfeld apologizes for the 'uncomfortable subtle sexual aspect' between a human and an insect in 'Bee Movie'",
                    "link": "https://news.yahoo.com/jerry-seinfeld-apologizes-uncomfortable-subtle-203443120.html",
                    "description": None,
                    "author": None,
                    "category": None,
                    "comments": None,
                    "enclosure": None,
                    "guid": {
                        "is_perm_link": False,
                        "text": "jerry-seinfeld-apologizes-uncomfortable-subtle-203443120.html",
                    },
                    "pub_date": datetime(2021, 10, 3, 20, 34, 43, tzinfo=tzutc()),
                    "source": {"url": "https://www.insider.com/", "text": "INSIDER"},
                },
            ],
        },
    }

    return DictContentWrapper(rss_dict)
