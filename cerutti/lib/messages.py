from typing import ClassVar, List, Type, Dict

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
    # The number of runs of the auction
    runs: int

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


@dataclass
class MultiAuctionEnd:
    winners: Dict[str, int]
    Schema: ClassVar[Type[Schema]] = Schema


@dataclass
class ResetBot:
    reset: str
    Schema: ClassVar[Type[Schema]] = Schema
