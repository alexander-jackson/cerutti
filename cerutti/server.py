#!/usr/bin/env python3

import asyncio
import websockets

from dataclasses import dataclass
from typing import Dict, Type, List, Tuple, Union

from zenlog import log

from cerutti.lib.auctioneer import Auctioneer
from cerutti.lib.user_bot import UserBot
from cerutti.lib.messages import AuctionEnd, Registration, MultiAuctionEnd, ResetBot

Room = List[UserBot]

event = asyncio.Event()


@dataclass
class SingleRoom:
    winners: List[str]
    room: Room

    def add(self, bot: UserBot):
        self.bot_room.append(bot)


@dataclass
class MultiRoom:
    winners: Dict[str, int]
    bot_room: Room
    runs: int

    def add(self, bot: UserBot):
        self.bot_room.append(bot)
        self.winners[bot.name] = 0


@dataclass(unsafe_hash=True)
class RoomKey:
    gametype: str
    bots: int
    room_type: Type[Union[SingleRoom, MultiRoom]]


@dataclass
class RoomInfo:
    has_run: bool
    room_type: Type[Union[SingleRoom, MultiRoom]]
    event: asyncio.Event
    finished: int


rooms: Dict[RoomKey, Tuple[asyncio.Lock, Union[SingleRoom, MultiRoom], RoomInfo]] = {}


async def _run_auction(
    room_key: RoomKey,
    room_info: RoomInfo,
    room: Union[SingleRoom, MultiRoom],
    websocket,
):

    if room_info.room_type is MultiRoom:

        log.debug("Running multiroom")
        for _ in range(room.runs):
            auctioneer = Auctioneer(
                room=room.bot_room,
                game_type=room_key.gametype,
                slowdown=0,
                verbose=True,
            )
            winners = await auctioneer.run_auction()

            for winner in winners:
                room.winners[winner] += 1

            log.debug(f"Winners: {room.winners}")

            message = ResetBot.Schema().dumps(ResetBot(reset="RESET"))
            await websocket.send(message)
    else:
        auctioneer = Auctioneer(
            room=room.bot_room,
            game_type=room_key.gametype,
            slowdown=0,
            verbose=True,
        )
        log.info("running normal room")
        winners = await auctioneer.run_auction()
        log.info(f"Winners: {room.winners}")

    room_info.has_run = True


async def root(websocket, path):
    message = await websocket.recv()
    registration = Registration.Schema().loads(message)
    log.debug(f"Received a connection with settings={registration}")

    room_type = MultiRoom if registration.runs > 1 else SingleRoom
    key = RoomKey(
        gametype=registration.gametype, bots=registration.bots, room_type=room_type
    )
    # Ensure the room exists

    if key not in rooms:
        log.debug(f"Adding room_key={key} to the state")

        room = (
            MultiRoom(winners={}, bot_room=[], runs=registration.runs)
            if room_type is MultiRoom
            else SingleRoom(winners=[], bot_room=[])
        )

        rooms[key] = (
            asyncio.Lock(),
            room,
            RoomInfo(
                has_run=False,
                event=asyncio.Event(),
                finished=0,
                room_type=room_type,
            ),
        )

    # Get the room itself and add the current client
    lock, room, info = rooms[key]
    if info.room_type is MultiRoom:
        room.runs = min(room.runs, registration.runs)

    room.add(UserBot(registration.name, websocket))

    greeting = f"Hello {registration.name}, there are currently {len(room.bot_room)} bots playing!"

    await websocket.send(greeting)

    # If we don't have enough bots, wait until we do
    if len(room.bot_room) < key.bots:
        log.debug(f"Room with key={key} has too few bots currently")
        await info.event.wait()

    # We have enough, notify all tasks
    info.event.set()

    async with lock:
        if not info.has_run:
            log.debug(f"Beginning auction for key={key}")

            await _run_auction(
                room_key=key, room_info=info, room=room, websocket=websocket
            )
            # Create the auctioneer and begin
            # auctioneer = Auctioneer(
            #     room=room,
            #     game_type=key.gametype,
            #     slowdown=0,
            #     verbose=True,
            # )

            # info.winners = await auctioneer.run_auction()
            # log.info(f"Winners: {info.winners}")

            # info.has_run = True

        info.finished += 1

    if info.room_type is MultiRoom:
        auction_end = MultiAuctionEnd(winners=room.winners)
        message = MultiAuctionEnd.Schema().dumps(auction_end)
    else:
        auction_end = AuctionEnd(winners=room.winners)
        message = AuctionEnd.Schema().dumps(auction_end)

    # If all sockets have informed their clients, delete the room
    if info.finished == key.bots:
        log.debug(f"All {info.finished} clients have been informed, deleting key={key}")
        del rooms[key]

    # Game has been run now, inform the sockets
    await websocket.send(message)


def start(args):
    log.info(f"Hosting a server on port: {args.port}")
    start_server = websockets.serve(root, "127.0.0.1", args.port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
