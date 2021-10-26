import logging
import os
import warnings
from dataclasses import asdict
from datetime import datetime
from typing import Sequence

import requests
from bs4 import BeautifulSoup
from colorama import init
from urllib3.exceptions import InsecureRequestWarning

from rss_parser.base import IParser, BaseStorage, IContentWrapper
from rss_parser.content_wrapper import Bs4ContentWrapper, DictContentWrapper
from rss_parser.converter import get_json_text, get_text, get_html_text, save_pdf_to_file
from rss_parser.exceptions import ResolveError
from rss_parser.parser import RSSParser
from rss_parser.schema import Channel, ConsoleArgs
from rss_parser.storage import FileStorage
from rss_parser.utils import is_valid_url, init_argparse, get_console_handler, convert_namespace_to_dataclass

logging.basicConfig(
    filename="log.log", filemode="w", format="%(name)s - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(level=logging.WARNING)
logging.getLogger("xhtml2pdf").setLevel(level=logging.WARNING)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def process_rss(
    console_args: ConsoleArgs, parser: IParser, storage: BaseStorage, content_wrappers: Sequence[IContentWrapper]
) -> None:
    channels = []
    for i, content_wrapper in enumerate(content_wrappers):
        logger.debug("Parse the received data.")
        try:
            channel = parser.parse_by_dataclass(content_wrapper, Channel)
            channels.append(channel)
        except ResolveError as e:
            logger.info(e)
            continue

        if console_args.source is not None and console_args.date is None:
            logger.debug("Save data to storage.")
            urls_in_storage = storage.setdefault(datetime.now().strftime("%Y%m%d"), {})
            news_in_storage = urls_in_storage.setdefault(console_args.source, [])
            news_in_storage.append(asdict(channel))

        if console_args.limit is not None:
            logger.debug("Limiting {} elements to {}.".format(len(channel.items), console_args.limit))
            channel.items = channel.items[: console_args.limit]

        value_to_print = get_json_text(channel) if console_args.json else get_text(channel)

        logger.debug("Output {} data to stdout.".format(i + 1))
        logger.info(value_to_print)

    html_str = get_html_text(channels)

    if console_args.to_html is not None:
        logger.debug("Save html content to the file.")
        try:
            with open(console_args.to_html, "w", encoding="utf-8") as f:
                f.write(html_str)
        except FileNotFoundError:
            logger.info("Wrong path to save html in the file")

    if console_args.to_pdf is not None:
        logger.debug("Save pdf content to the file.")
        try:
            save_pdf_to_file(console_args.to_pdf, html_str)
        except FileNotFoundError:
            logger.info("Wrong path to save pdf in the file")


def main():
    init()

    namespace = init_argparse().parse_args()
    console_args = convert_namespace_to_dataclass(namespace, ConsoleArgs)

    parser = RSSParser()
    storage = FileStorage(os.path.join(os.getcwd(), "cache.txt"))

    console_handler = get_console_handler(console_args.verbose, console_args.colorize)
    logging.root.addHandler(console_handler)

    if console_args.date is not None:
        logger.debug("Get data from storage for {} date.".format(console_args.date))
        content = storage.get(console_args.date, {})
        if console_args.source is not None:
            data = content.get(console_args.source)
        else:
            data = [item for key in content.keys() for item in content.get(key)]

        if data is None:
            logger.info("Could not find data.")
            return None

        content_wrappers = [DictContentWrapper(content) for content in data]
    else:
        if not is_valid_url(console_args.source):
            logger.info("Could not find data.")
            return None

        logger.debug("Get data from {} url.".format(console_args.source))
        response = requests.get(console_args.source, verify=False)
        if not response.ok:
            logger.info("Could not find data.")
            return None

        content = response.text
        data = content[content.find("?>") + 2 :] if content[:5] == "<?xml" else content
        bs4_soup = BeautifulSoup(data, "xml")
        channel_tag = bs4_soup.find("channel")
        if channel_tag is None:
            logger.info("Could not find data.")
            return None

        content_wrappers = [Bs4ContentWrapper(channel_tag)]

    try:
        process_rss(console_args, parser, storage, content_wrappers)
    except Exception as e:
        logger.info("The program stopped with an unhandled error: {}".format(e))
    finally:
        storage.save()
        storage.close()


if __name__ == "__main__":
    main()
