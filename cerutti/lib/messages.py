from typing import ClassVar, List, Type

from marshmallow import Schema
from marshmallow_dataclass import dataclass


@dataclass
class Registration:
    # The name of the user's bot
    name: str
    # The gametype they would like to play
    gametype: str
    # The number of bots to wait for
    bots: int

    # For the type checker
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
