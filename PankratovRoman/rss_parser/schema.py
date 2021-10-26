"""Contains schema(dataclasses) for parsing content."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class Source:
    url: str
    text: str


@dataclass
class Enclosure:
    url: str
    length: int
    type: str


@dataclass
class Category:
    domain: Optional[str]
    text: str


@dataclass
class Guid:
    is_perm_link: Optional[bool] = field(metadata={"tag_names": ["isPermaLink"]})
    text: str


@dataclass
class Content:
    url: Optional[str]
    width: Optional[int]
    height: Optional[int]


@dataclass
class Item:
    title: Optional[str]
    link: Optional[str]
    description: Optional[str]
    author: Optional[str]
    category: Optional[Category]
    comments: Optional[str]
    enclosure: Optional[Enclosure]
    guid: Optional[Guid]
    pub_date: Optional[datetime] = field(metadata={"tag_names": ["pubDate"]})
    source: Optional[Source]
    content: Optional[Content] = field(metadata={"tag_names": ["media:content"]})


@dataclass
class TextInput:
    title: str
    description: str
    name: str
    link: str


@dataclass
class Cloud:
    domain: str
    port: int
    path: str
    register_procedure: str = field(metadata={"tag_names": ["registerProcedure"]})
    protocol: str


@dataclass
class Image:
    title: str
    link: str
    url: str
    description: Optional[str]
    width: Optional[int]
    height: Optional[int]


@dataclass
class Channel:
    title: str
    link: str
    description: str
    language: Optional[str]
    copyright: Optional[str]
    managing_editor: Optional[str] = field(metadata={"tag_names": ["managingEditor"]})
    web_master: Optional[str] = field(metadata={"tag_names": ["webMaster"]})
    pub_date: Optional[datetime] = field(metadata={"tag_names": ["pubDate"]})
    last_build_date: Optional[datetime] = field(metadata={"tag_names": ["lastBuildDate"]})
    category: Optional[str]
    generator: Optional[str]
    docs: Optional[str]
    ttl: Optional[int]
    image: Optional[Image]
    cloud: Optional[Cloud]
    rating: Optional[str]
    text_input: Optional[TextInput] = field(metadata={"tag_names": ["textInput"]})
    items: List[Item] = field(metadata={"tag_names": ["item"]})


@dataclass
class Rss:
    version: str
    channel: Channel


@dataclass(frozen=True)
class ConsoleArgs:
    source: Optional[str]
    date: Optional[str]
    limit: Optional[int]
    json: bool
    verbose: bool
    colorize: bool
    to_html: Optional[str]
    to_pdf: Optional[str]
