#!/usr/bin/env python3

import random
import asyncio
import websockets

from copy import deepcopy
from typing import Dict, List

from auctioneer import Auctioneer

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

    async def get_bid_game_type_collection(
        self,
        current_round: int,
        bots,
        game_type: str,
        winner_pays: int,
        artists_and_values: Dict[str, int],
        round_limit: int,
        starting_budget: int,
        painting_order: List[str],
        target_collection: List[int],
        my_bot_details,
        current_painting: str,
        winner_ids: List[str],
        amounts_paid: List[int],
    ) -> int:
        await self.websocket.send(f"Current round: {current_round}")
        return 0

    async def get_bid_game_type_value(
        self,
        current_round: int,
        bots,
        game_type: str,
        winner_pays: int,
        artists_and_values: Dict[str, int],
        round_limit: int,
        starting_budget: int,
        painting_order: List[str],
        target_collection: List[int],
        my_bot_details,
        current_painting: str,
        winner_ids: List[str],
        amounts_paid: List[int],
    ) -> int:
        await self.websocket.send(f"Current round: {current_round}")
        return 0

    def __deepcopy__(self, memo):
        return UserBot(deepcopy(self.name, memo), self.websocket)


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
                room=room, game_type="value", slowdown=0, verbose=False
            )
            winners = await auctioneer.run_auction()
            print("winners: {}".format(winners))

            game_has_been_run = True

    # Game has been run now, inform the sockets
    await websocket.send(winners[0])


def main():
    start_server = websockets.serve(root, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
