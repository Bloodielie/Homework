"""Contains functions for converting content."""

import json
import logging
from dataclasses import asdict
from typing import Dict, Any

from rss_parser.schema import Channel
from rss_parser.types import DataClassType

logger = logging.getLogger(__name__)

CHANNEL_TEXT = """Channel:
    Title: {title}
    Description: {description}
    Date: {date}
    Link: {link}
    Image: {image_url}

Items:"""

ITEM = """
    Number: {number}    
    Title: {title}
    Description: {description}
    Date: {date}
    Link: {link}
    Content: {content_url}
"""


def get_dict(dataclass_: DataClassType) -> Dict[str, Any]:
    """Converts dataclass to dict."""

    logger.debug("Convert {} to dict.".format(dataclass_.__class__))
    dict_result = asdict(dataclass_)
    return json.loads(json.dumps(dict_result, default=str))


def get_text(channel: Channel) -> str:
    """Converts channel dataclass to string."""

    logger.debug("Convert {} to string.".format(channel.__class__))
    result = CHANNEL_TEXT.format(
        title=channel.title,
        link=channel.link,
        description=channel.description,
        date=channel.pub_date,
        image_url=getattr(channel.image, "url", None),
    )
    return result + "".join(
        ITEM.format(
            number=i + 1,
            title=item.title,
            link=item.link,
            description=item.description,
            date=item.pub_date,
            content_url=getattr(item.content, "url", None),
        )
        for i, item in enumerate(channel.items)
    )
