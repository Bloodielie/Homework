import os
import re
from typing import List

from setuptools import setup, find_packages


def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """Return the README."""
    with open("README.md", "r", encoding="utf8") as f:
        return f.read()


def get_requirements(path: str) -> List[str]:
    """Return requirements from file.

    Args:
        path: Path to file.

    Return:
        List of requirements.
    """
    with open(path, "r", encoding="utf8") as f:
        data = f.read()

    return data.split("\n")


setup(
    name="rss-reader",
    python_requires=">=3.9",
    version=get_version("rss_parser"),
    url="https://github.com/Bloodielie/Homework/tree/master/PankratovRoman",
    author="Roma Pankratov",
    author_email="riopro2812@gmail.com",
    description="Python command-line RSS reader",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages('rss_parser'),
    include_package_data=True,
    install_requires=get_requirements("./requirements.txt"),
    entry_points={
        'console_scripts': ['rss_reader = main:main']
    }
)
