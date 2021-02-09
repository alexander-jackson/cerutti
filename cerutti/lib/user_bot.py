#!/usr/bin/env python3

import pickle

from copy import deepcopy


class UserBot(object):
    def __init__(self, name: str, websocket):
        self.name = name
        self.websocket = websocket

    def Bot(self):
        print(self.name)
        return self

    async def get_bid_game_type_collection(self, args) -> int:
        await self.websocket.send(f"Current round: {current_round}")
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
