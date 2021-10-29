"""This module combines all the other modules and provides entry to RSS processing from the command line.

Example:
    python main.py https://news.yahoo.com/rss/ --limit 5 --json --colorize
    python main.py https://vse.sale/news/rss --limit 5 --to-html test.html
    python main.py https://lenta.ru/rss/top7 --limit 5 --verbose
"""

import logging
import os
import warnings
from dataclasses import asdict
from datetime import datetime
from typing import Sequence

from colorama import init
from rss_parser.base import IParser, BaseStorage, IContentWrapper
from rss_parser.content_getter import StorageContentGetter, InternetContentGetter
from rss_parser.converter import get_json_text, get_text, get_html_text, save_pdf_to_file
from rss_parser.exceptions import ResolveError
from rss_parser.parser import RSSParser
from rss_parser.schema import Channel, ConsoleArgs
from rss_parser.storage import FileStorage
from rss_parser.utils import is_valid_url, init_argparse, get_console_handler, convert_namespace_to_dataclass
from urllib3.exceptions import InsecureRequestWarning

logging.basicConfig(
    filename="log.log", filemode="w", format="%(name)s - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(level=logging.WARNING)
logging.getLogger("xhtml2pdf").setLevel(level=logging.WARNING)
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def process_rss(
    console_args: ConsoleArgs, parser: IParser, storage: BaseStorage, content_wrappers: Sequence[IContentWrapper]
):
    """Performs main RSS processing.

    Args:
        console_args: Arguments parsed from the console.
        parser: Class for parsing content.
        storage: Local data storage.
        content_wrappers: Content wrapper for consistent work.
    """
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
    """The entry point to the program doing some preparation and starting rss processing."""
    init()

    namespace = init_argparse().parse_args()
    console_args = convert_namespace_to_dataclass(namespace, ConsoleArgs)

    parser = RSSParser()
    storage = FileStorage(os.path.join(os.getcwd(), "cache.txt"))

    console_handler = get_console_handler(console_args.verbose, console_args.colorize)
    logging.root.addHandler(console_handler)

    if console_args.date is not None:
        content_getter = StorageContentGetter(storage)
    elif not is_valid_url(console_args.source):
        logger.info("You have passed the wrong url.")
        return None
    else:
        content_getter = InternetContentGetter()

    logger.debug("Receive content.")
    content_wrappers = content_getter.get_content_wrappers(console_args)
    if content_wrappers is None:
        logger.debug("Failed to get content.")
        return None

    try:
        process_rss(console_args, parser, storage, content_wrappers)
    except Exception as e:
        logger.info("The program stopped with an unhandled error: {}".format(e))
    finally:
        storage.save()
        storage.close()


if __name__ == "__main__":
    main()
