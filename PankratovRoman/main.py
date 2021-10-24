import logging
import os
from dataclasses import asdict
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper
from rss_parser.converter import get_json_text, get_text, get_html_text, save_pdf_to_file
from rss_parser.exceptions import ResolveError
from rss_parser.parser import RSSParser
from rss_parser.schema import Rss
from rss_parser.storage import FileStorage
from rss_parser.utils import is_valid_url, init_argparse

logging.basicConfig(
    filename="log.log", filemode="w", format="%(name)s - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(level=logging.WARNING)
logging.getLogger("xhtml2pdf").setLevel(level=logging.WARNING)


def main():
    console_args = init_argparse().parse_args()

    parser = RSSParser()
    storage = FileStorage(os.path.join(os.getcwd(), "cache.txt"))

    if console_args.verbose:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(logging.Formatter("%(name)s - %(asctime)s - %(message)s"))
        logging.root.addHandler(console_handler)

    if console_args.date is not None:
        logger.debug("Get data from storage for {} date.".format(console_args.date))
        content = storage.get(console_args.date, {})
        if console_args.source is not None:
            data = content.get(console_args.source)
        else:
            data = [item for key in content.keys() for item in content.get(key)]

        if data is None:
            print("Could not find data.")
            return None

        content_wrappers = [DictContentWrapper(content) for content in data]
    else:
        if not is_valid_url(console_args.source):
            print("Invalid RSS URL address.")
            return None

        logger.debug("Get data from {} url.".format(console_args.source))
        response = requests.get(console_args.source, verify=False)
        if not response.ok:
            print("Failed to get RSS data.")
            return None

        content = response.text
        data = content[content.find("?>") + 2 :] if content[:5] == "<?xml" else content
        bs4_soup = BeautifulSoup(data, "xml")
        rss_tag = bs4_soup.find("rss")
        if rss_tag is None:
            print("Invalid rss content.")
            return None

        content_wrappers = [Bs4ContentWrapper(rss_tag)]

    parsing_results = []
    for i, content_wrapper in enumerate(content_wrappers):
        logger.debug("Parse the received data.")
        try:
            result = parser.parse_by_dataclass(content_wrapper, Rss)
            parsing_results.append(result)
        except ResolveError as e:
            print(e)
            continue

        if console_args.source is not None and console_args.date is None:
            logger.debug("Save data to storage.")
            urls_in_storage = storage.setdefault(datetime.now().strftime("%Y%m%d"), {})
            news_in_storage = urls_in_storage.setdefault(console_args.source, [])
            news_in_storage.append(asdict(result))

        if console_args.limit is not None:
            logger.debug("Limiting {} elements to {}.".format(len(result.channel.items), console_args.limit))
            result.channel.items = result.channel.items[: console_args.limit]

        value_to_print = get_json_text(result.channel) if console_args.json else get_text(result.channel)

        logger.debug("Output {} data to stdout.".format(i + 1))
        print(value_to_print)

    html_str = get_html_text([result.channel for result in parsing_results])

    if console_args.to_html is not None:
        logger.debug("Save html content to the file.")
        try:
            with open(console_args.to_html, "w", encoding="utf-8") as f:
                f.write(html_str)
        except FileNotFoundError:
            print("Wrong path to save html in the file")

    if console_args.to_pdf is not None:
        logger.debug("Save pdf content to the file.")
        try:
            save_pdf_to_file(console_args.to_pdf, html_str)
        except FileNotFoundError:
            print("Wrong path to save pdf in the file")

    storage.save()
    storage.close()


if __name__ == "__main__":
    main()
