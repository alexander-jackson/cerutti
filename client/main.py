#!/usr/bin/env python3

import asyncio
import websockets


async def hello():
    uri = "ws://localhost:8765"

    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

        # Wait until the game begins
        while True:
            message = await websocket.recv()
            print("message: {}".format(message))


asyncio.get_event_loop().run_until_complete(hello())
