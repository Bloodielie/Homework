import logging
from argparse import ArgumentParser
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from rss_parser import __version__
from rss_parser.content_wrapper import Bs4ContentWrapper
from rss_parser.converter import get_dict, get_text
from rss_parser.exceptions import ResolveError
from rss_parser.parser import RSSParser
from rss_parser.schema import Rss
from rss_parser.utils import is_valid_url

logging.basicConfig(
    filename="log.log", filemode="w", format="%(name)s - %(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)
logging.getLogger("urllib3").setLevel(level=logging.WARNING)


def main():
    console_args_parser = ArgumentParser(description="Python command-line RSS reader.")
    console_args_parser.add_argument("--version", action="version", version=f"Version {__version__}")
    console_args_parser.add_argument(
        "--json", default=False, action="store_true", help="Print result as JSON in stdout"
    )
    console_args_parser.add_argument(
        "--verbose", default=False, action="store_true", help="Outputs verbose status messages"
    )
    console_args_parser.add_argument(
        "--limit", metavar="LIMIT", type=int, help="Limit news topics if this parameter provided"
    )
    console_args_parser.add_argument("source", type=str, help="RSS URL")
    console_args = console_args_parser.parse_args()

    if not is_valid_url(console_args.source):
        print("Invalid RSS URL address.")
        return None

    if console_args.verbose:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter("%(name)s - %(asctime)s - %(message)s"))
        logging.root.addHandler(console)

    logger.debug("Get data from {} url.".format(console_args.source))
    response = requests.get(console_args.source)
    if not response.ok:
        print("Failed to get RSS data.")
        return None

    data = response.text
    if data[:5] == "<?xml":
        data = data[data.find("?>") + 2 :]

    parser = RSSParser()
    bs4_soup = BeautifulSoup(data, "xml")

    logger.debug("Get rss tag from data.")
    rss_tag = bs4_soup.find("rss")
    if rss_tag is None:
        print("Invalid rss content.")
        return None

    content_wrapper = Bs4ContentWrapper(rss_tag)
    try:
        logger.debug("Parse the received data.")
        result = parser.parse_by_dataclass(content_wrapper, Rss)
    except ResolveError as e:
        print(e)
        return None

    if console_args.limit is not None:
        logger.debug("Limiting {} elements to {}.".format(len(result.channel.items), console_args.limit))
        result.channel.items = result.channel.items[: console_args.limit]

    logger.debug("Output data to stdout.")
    if console_args.json:
        pprint(get_dict(result.channel))
    else:
        print(get_text(result.channel))


if __name__ == "__main__":
    main()
