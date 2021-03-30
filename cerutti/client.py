#!/usr/bin/env python3

import pickle
import asyncio
import websockets

from typing import Optional, Union

from zenlog import log

from cerutti.player import Bot
from cerutti.lib.messages import (
    AuctionEnd,
    BidRequest,
    Registration,
    MultiAuctionEnd,
    ResetBot,
)

# Create a bot for the user
bot = Bot()


async def parse_game_message(websocket) -> Optional[Union[BidRequest, AuctionEnd]]:
    data = await websocket.recv()

    types = [BidRequest, AuctionEnd, MultiAuctionEnd, ResetBot]

    for ty in types:
        try:
            message = ty.Schema().loads(data)
            return message
        except Exception:
            continue


async def play_game(websocket, gametype: str):
    # Wait until the game begins
    global bot
    while True:
        message = await parse_game_message(websocket)

        if message is None:
            log.error("Failed to get a valid message from the socket.")
            continue

        if isinstance(message, BidRequest):
            args = pickle.loads(bytes.fromhex(message.arguments))
            value = None

            if gametype == "value":
                value = str(bot.get_bid_game_type_value(**args))
            else:
                value = str(bot.get_bid_game_type_collection(**args))

            await websocket.send(value)
        elif isinstance(message, (AuctionEnd, MultiAuctionEnd)):
            log.info(f"Auction winners: {message.winners}")
            return
        elif isinstance(message, ResetBot):
            log.info("Resetting bot")
            bot = Bot()


async def main(args):
    uri = f"ws://{args.base}"

    if args.port:
        uri = f"{uri}:{args.port}"

    log.info(f"Connecting to: {uri}")

    async with websockets.connect(uri) as websocket:
        registration = Registration(
            name=bot.name, gametype=args.gametype, bots=args.bots, runs=args.runs
        )
        message = Registration.Schema().dumps(registration)

        log.debug(f"Sending to the server: {message}")
        await websocket.send(message)

        greeting = await websocket.recv()
        log.info(f"< {greeting}")

        await play_game(websocket, args.gametype)


def start(args):
    asyncio.get_event_loop().run_until_complete(main(args))
