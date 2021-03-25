#!/usr/bin/env python3

import asyncio
import websockets

from zenlog import log

from cerutti.lib.auctioneer import Auctioneer
from cerutti.lib.user_bot import UserBot
from cerutti.lib.messages import AuctionEnd, Registration

auctioneer = None
room = []
winners = []
event = asyncio.Event()
game_lock = asyncio.Lock()
game_has_been_run = False


async def root(websocket, path):
    global game_has_been_run, winners

    message = await websocket.recv()
    registration = Registration.Schema().loads(message)
    log.debug(f"Received a connection with settings={registration}")

    greeting = (
        f"Hello {registration.name}, there are currently {len(room)} bots playing!"
    )
    await websocket.send(greeting)

    room.append(UserBot(registration.name, websocket))

    # If we don't have enough bots, wait until we do
    if len(room) < registration.bots:
        await event.wait()

    # We have enough, notify all tasks
    event.set()

    async with game_lock:
        if not game_has_been_run:
            # Create the auctioneer and begin
            auctioneer = Auctioneer(
                room=room, game_type=registration.gametype, slowdown=0, verbose=True
            )
            winners = await auctioneer.run_auction()
            log.info(f"Winners: {winners}")

            game_has_been_run = True

    registration = AuctionEnd(winners=winners)
    message = AuctionEnd.Schema().dumps(registration)

    # Game has been run now, inform the sockets
    await websocket.send(message)


def start(args):
    log.info(f"Hosting a server on port: {args.port}")
    start_server = websockets.serve(root, "localhost", args.port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
