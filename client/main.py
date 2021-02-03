#!/usr/bin/env python3

import pickle
import random
import asyncio
import websockets

from uXXXXXXX import Bot
from server import UserBot

# Create a bot for the user
bot = Bot()


async def main():
    uri = "ws://abs.blackboards.pl:8765"

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


asyncio.get_event_loop().run_until_complete(main())
