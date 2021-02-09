#!/usr/bin/env python3

import pickle
import random
import asyncio
import websockets

from copy import deepcopy
from typing import Dict, List

from cerutti.lib.auctioneer import Auctioneer

auctioneer = None
room = []
winners = []
event = asyncio.Event()
game_lock = asyncio.Lock()
game_has_been_run = False


class UserBot(object):
    def __init__(self, name: str, websocket):
        self.name = name
        self.websocket = websocket

    def Bot(self):
        print(self.name)
        return self

    async def get_bid_game_type_collection(self, args) -> int:
        await self.websocket.send(pickle.dumps(args))
        return int(await self.websocket.recv())

    async def get_bid_game_type_value(self, args) -> int:
        # Convert the dictionary to a JSON string
        await self.websocket.send(pickle.dumps(args))
        return int(await self.websocket.recv())

    def __deepcopy__(self, memo):
        return UserBot(deepcopy(self.name, memo), self.websocket)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["websocket"]
        return state


async def root(websocket, path):
    global game_has_been_run, winners

    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}, there are currently {len(room)} bots playing!"
    await websocket.send(greeting)

    identifier = len(room)
    room.append(UserBot(name, websocket))

    # If we don't have enough bots, wait until we do
    if len(room) < 2:
        await event.wait()

    # We have enough, notify all threads
    event.set()

    async with game_lock:
        if not game_has_been_run:
            # Create the auctioneer and begin
            auctioneer = Auctioneer(
                room=room, game_type="value", slowdown=0, verbose=True
            )
            winners = await auctioneer.run_auction()
            print("winners: {}".format(winners))

            game_has_been_run = True

    # Game has been run now, inform the sockets
    await websocket.send(winners[0])


def start():
    start_server = websockets.serve(root, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
