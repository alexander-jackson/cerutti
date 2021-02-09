#!/usr/bin/env python3

import argparse
import pickle
import random
import asyncio
import websockets

from cerutti.player import Bot
from cerutti.lib.server import UserBot

# Create a bot for the user
bot = Bot()


async def main():
    uri = f"ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

        # Wait until the game begins
        while True:
            message = pickle.loads(await websocket.recv())
            await websocket.send(str(bot.get_bid_game_type_value(**message)))


def start():
    asyncio.get_event_loop().run_until_complete(main())
