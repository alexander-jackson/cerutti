from typing import ClassVar, List, Type

from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class Registration:
    name: str
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class BidRequest:
    # hex-encoded string
    arguments: str
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class AuctionEnd:
    winners: List[str]
    Schema: ClassVar[Type[Schema]] = Schema
