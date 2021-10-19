"""A module that includes various utilities."""

from argparse import Action
from typing import Union
from urllib.parse import urlparse


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
