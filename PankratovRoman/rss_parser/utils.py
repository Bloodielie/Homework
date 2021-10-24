"""A module that includes various utilities."""
import argparse
from typing import Union
from urllib.parse import urlparse

from rss_parser import __version__


def is_optional_typing(annotation) -> bool:
    """Checks annotation for Optional.

    Args:
        annotation: Annotation to check.

    Return:
        Annotation is Optional.
    """
    origin = getattr(annotation, "__origin__", None)
    if origin is Union and annotation.__args__[-1] is type(None):
        return True

    return False


def is_list_typing(annotation) -> bool:
    """Checks annotation for List typing.

    Args:
        annotation: Annotation to check.

    Return:
        Annotation is List typing.
    """
    annotation_type_name = getattr(annotation, "_name", "")
    if annotation_type_name == "List":
        return True
    return False


def is_valid_url(url: str) -> bool:
    """Checks the validity of the url.

    Args:
        url: Url to check.

    Return:
        If the url is valid return True.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def init_argparse() -> argparse.ArgumentParser:
    """Initialize argparse arguments.

    Returns:
        Parsed arguments.
    """
    console_args_parser = argparse.ArgumentParser(description="Python command-line RSS reader.")
    console_args_parser.add_argument(
        "--version", action="version", version=f"Version {__version__}", help="Prints version info"
    )
    console_args_parser.add_argument(
        "--json", default=False, action="store_true", help="Print result as JSON in stdout"
    )
    console_args_parser.add_argument(
        "--verbose", default=False, action="store_true", help="Outputs verbose status messages"
    )
    console_args_parser.add_argument(
        "--limit", metavar="LIMIT", type=int, help="Limit news topics if this parameter provided"
    )
    console_args_parser.add_argument("--date", nargs="?", type=str, help="Outputs rss feed for the specified date")
    console_args_parser.add_argument("--to-html", type=str, help="Saves news in html format along the specified path.")
    console_args_parser.add_argument("--to-pdf", type=str, help="Saves news in pdf format along the specified path.")
    console_args_parser.add_argument("source", nargs="?", type=str, help="RSS URL")
    return console_args_parser
