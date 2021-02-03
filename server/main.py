#!/usr/bin/env python3

import asyncio
import websockets

from typing import Dict, List

from auctioneer import Auctioneer

auctioneer = None
room = []
event = asyncio.Event()


class UserBot(object):
    def __init__(self, name: str):
        self.name = name

    def Bot(self):
        print(self.name)
        return self

    def get_bid_game_type_collection(
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
        return 0

    def get_bid_game_type_value(
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
        return 0


async def root(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}, there are currently {len(room)} bots playing!"
    await websocket.send(greeting)

    room.append(UserBot(name))
    print("bots: {}".format(room))

    # If we don't have enough bots, wait until we do
    if len(room) < 2:
        await event.wait()

    # We have enough, notify all threads
    event.set()

    await websocket.send("Game is beginning, bot count has been achieved")

    # Create the auctioneer and begin
    auctioneer = Auctioneer(room=room, game_type="value", slowdown=0)
    auctioneer.run_auction()


def main():
    start_server = websockets.serve(root, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
