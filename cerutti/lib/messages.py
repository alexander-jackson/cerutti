from marshmallow_dataclass import dataclass


@dataclass
class Registration:
    name: str


@dataclass
class BidRequest:
    # hex-encoded string
    arguments: str