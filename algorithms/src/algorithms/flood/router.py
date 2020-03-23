#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements router interface for network flooding algorithm
"""

import asyncio

import interface

class Router(interface.Router):
    """
    Implements Router interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine
            if a message is stale
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clocks = {}

    async def on_recv(self, trx, msg):
        header, data = msg
        uid, clock, topic = header
        # check for stale message
        if uid in self.clocks:
            if clock <= self.clocks[uid]:
                # old publish message, don't do anything
                await self.log(("rejected", topic, data))
                return
        # update message to most recent
        self.clocks[uid] = clock
        # broadcast message to all channels
        await self.log(("accepted", topic, data))
        await asyncio.gather(*(t.transmit(msg) for t in self.trxs))
