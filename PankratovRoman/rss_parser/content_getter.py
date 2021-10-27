import logging
from typing import Optional, Sequence

import requests
from bs4 import BeautifulSoup

from rss_parser.base import BaseStorage, IContentWrapper, IContentGetter
from rss_parser.content_wrapper import DictContentWrapper, Bs4ContentWrapper
from rss_parser.schema import ConsoleArgs

logger = logging.getLogger(__name__)


class StorageContentGetter(IContentGetter):
    """Class for getting content from storage.

    Args:
        storage: Data store for receiving content.
    """

    def __init__(self, storage: BaseStorage):
        self._storage = storage

    def get_content_wrappers(self, console_args: ConsoleArgs) -> Optional[Sequence[IContentWrapper]]:
        """Receives content from storage and wraps it in DictContentWrapper."""

        content = self._storage.get(console_args.date)
        if content is None:
            logger.debug("Could not find data by date.")
            return None

        if console_args.source is not None:
            data = content.get(console_args.source)
        else:
            data = [item for key in content.keys() for item in content.get(key)]

        if data is None:
            logger.debug("Could not find data.")
            return None

        return tuple(DictContentWrapper(content) for content in data)


class InternetContentGetter(IContentGetter):
    """Class for getting content from internet."""

    def get_content_wrappers(self, console_args: ConsoleArgs) -> Optional[Sequence[IContentWrapper]]:
        """Receives content from internet and wraps it in Bs4ContentWrapper."""

        response = requests.get(console_args.source, verify=False)
        if not response.ok:
            logger.debug("The site did not submit content.")
            return None

        content = response.text
        data = content[content.find("?>") + 2:] if content[:5] == "<?xml" else content
        bs4_soup = BeautifulSoup(data, "xml")
        channel_tag = bs4_soup.find("channel")
        if channel_tag is None:
            logger.info("Couldn't find channel tag.")
            return None

        return [Bs4ContentWrapper(channel_tag)]
