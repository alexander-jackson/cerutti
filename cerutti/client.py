#!/usr/bin/env python3

import json
import pickle
import asyncio
import websockets

from zenlog import log

from cerutti.player import Bot
from cerutti.lib.user_bot import UserBot
from cerutti.lib.messages import Registration, BidRequest

# Create a bot for the user
bot = Bot()


async def main(args):
    uri = f"ws://{args.base}:{args.port}"
    log.info(f"Connecting to: {uri}")

    async with websockets.connect(uri) as websocket:
        registration = Registration(name=bot.name)
        message = Registration.Schema().dumps(registration)

        log.debug(f"Sending to the server: {message}")
        await websocket.send(message)

        greeting = await websocket.recv()
        log.info(f"< {greeting}")

        # Wait until the game begins
        while True:
            message = await websocket.recv()
            bid_request = BidRequest.Schema().loads(message)
            args = pickle.loads(bytes.fromhex(bid_request.arguments))

            await websocket.send(str(bot.get_bid_game_type_value(**args)))


def start(args):
    asyncio.get_event_loop().run_until_complete(main(args))
