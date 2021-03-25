#!/usr/bin/env python3

import json
import pickle

from copy import deepcopy

from cerutti.lib.messages import BidRequest


class UserBot(object):
    def __init__(self, name: str, websocket):
        self.name = name
        self.websocket = websocket

    def Bot(self):
        print(self.name)
        return self

    async def get_bid_game_type_collection(self, args) -> int:
        arguments = pickle.dumps(args).hex()
        bid_request = BidRequest(arguments=arguments)

        message = BidRequest.Schema().dump(bid_request)
        await self.websocket.send(json.dumps(message))

        return int(await self.websocket.recv())

    async def get_bid_game_type_value(self, args) -> int:
        arguments = pickle.dumps(args).hex()
        bid_request = BidRequest(arguments=arguments)

        message = BidRequest.Schema().dump(bid_request)
        await self.websocket.send(json.dumps(message))

        return int(await self.websocket.recv())

    def __deepcopy__(self, memo):
        return UserBot(deepcopy(self.name, memo), self.websocket)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["websocket"]
        return state
