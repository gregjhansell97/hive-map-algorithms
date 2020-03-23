#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements subscriber interface for network flooding algorithm
"""

import asyncio

import interface

class Subscriber(interface.Subscriber):
    """
    Implements Subscriber interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine if
            a message is stale
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clocks = {}

    async def on_recv(self, trx, msg):
        header, data = msg
        uid, clock, topic = header
        # not the right topic, subscriber doesn't care about it 
        if self.topic != topic:
            await self.log(("rejected", topic, data))
            return
        # check for stale messages
        if uid in self.clocks:
            if clock <= self.clocks[uid]:
                await self.log(("rejected", topic, data))
                return
        # update clock to most recent
        self.clocks[uid] = clock
        # invoke callback
        await asyncio.gather(
                self.log(("accepted", topic, data)), 
                self.callback(data))
