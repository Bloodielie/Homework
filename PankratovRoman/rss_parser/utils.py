"""A module that includes various utilities."""
import argparse
import logging
from typing import Union, Type, TypeVar
from urllib.parse import urlparse

from colorama import Fore

from rss_parser import __version__

T = TypeVar("T")


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
    console_args_parser.add_argument(
        "--colorize", default=False, action="store_true", help="Print colored messages to the console"
    )
    console_args_parser.add_argument("source", nargs="?", type=str, help="RSS URL")
    return console_args_parser


def get_console_handler(is_verbose: bool, is_colorize: bool) -> logging.StreamHandler:
    """Initialize stream handler.

    Args:
        is_verbose: Displays additional information.
        is_colorize: Colorizes messages.

    Returns:
        Configured stream handler.
    """
    if is_verbose:
        level = logging.DEBUG
        if is_colorize:
            output_format = f"{Fore.RED}%(name)s - {Fore.BLUE}%(asctime)s - {Fore.GREEN}%(message)s{Fore.RESET}"
        else:
            output_format = "%(name)s - %(asctime)s - %(message)s"
    else:
        level = logging.INFO
        output_format = f"{Fore.GREEN}%(message)s{Fore.RESET}" if is_colorize else "%(message)s"

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(output_format))
    return console_handler


def convert_namespace_to_dataclass(namespace: argparse.Namespace, dataclass: Type[T]) -> T:
    """Initialize dataclass by namespace fields.

    Args:
        namespace: Namespace for converting.
        dataclass: Dataclass for storing data.

    Returns:
        Initialized dataclass with namespace fields.
    """
    return dataclass(**vars(namespace))
