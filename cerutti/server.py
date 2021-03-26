#!/usr/bin/env python3

import asyncio
import websockets

from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple

from zenlog import log

from cerutti.lib.auctioneer import Auctioneer
from cerutti.lib.user_bot import UserBot
from cerutti.lib.messages import AuctionEnd, Registration

Room = List[UserBot]

event = asyncio.Event()


@dataclass
class RoomKey:
    gametype: str
    bots: int


@dataclass
class RoomInfo:
    has_run: bool
    winners: Optional[List[str]]
    event: asyncio.Event
    finished: int


rooms: Dict[RoomKey, Tuple[asyncio.Lock, Room, RoomInfo]] = {}


async def root(websocket, path):
    message = await websocket.recv()
    registration = Registration.Schema().loads(message)
    log.debug(f"Received a connection with settings={registration}")

    key = RoomKey(gametype=registration.gametype, bots=registration.bots)

    # Ensure the room exists
    if key not in rooms:
        log.debug(f"Adding room_key={key} to the state")

        rooms[key] = (
            asyncio.Lock(),
            [],
            RoomInfo(has_run=False, winners=None, event=asyncio.Event(), finished=0),
        )

    # Get the room itself and add the current client
    lock, room, info = rooms[key]
    room.append(UserBot(registration.name, websocket))

    greeting = (
        f"Hello {registration.name}, there are currently {len(room)} bots playing!"
    )

    await websocket.send(greeting)

    # If we don't have enough bots, wait until we do
    if len(room) < key.bots:
        log.debug(f"Room with key={key} has too few bots currently")
        await info.event.wait()

    # We have enough, notify all tasks
    info.event.set()

    async with lock:
        if not info.has_run:
            log.debug(f"Beginning auction for key={key}")

            # Create the auctioneer and begin
            auctioneer = Auctioneer(
                room=room,
                game_type=key.gametype,
                slowdown=0,
                verbose=True,
            )

            info.winners = await auctioneer.run_auction()
            log.info(f"Winners: {info.winners}")

            info.has_run = True

        info.finished += 1

    auction_end = AuctionEnd(winners=info.winners)
    message = AuctionEnd.Schema().dumps(auction_end)

    # If all sockets have informed their clients, delete the room
    if info.finished == key.bots:
        log.debug(f"All {info.finished} clients have been informed, deleting key={key}")
        del rooms[key]

    # Game has been run now, inform the sockets
    await websocket.send(message)


def start(args):
    log.info(f"Hosting a server on port: {args.port}")
    start_server = websockets.serve(root, "localhost", args.port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
