#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements router interface for network flooding algorithm
"""

import asyncio
import uuid

import interface
from interface import Transceiver


class Router(interface.Router):
    """
    Implements Router interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine
            if a message is stale
    """

    def __init__(self, *args, **kwargs):
        super().__init__(uuid.uuid4().bytes, *args, **kwargs)
        self.clocks = {}

    async def on_recv(self, trx: Transceiver, msg, context):
        header, data = msg
        clock_id, clock, topic = header
        # check for stale message
        if clock_id in self.clocks:
            if clock <= self.clocks[clock_id]:
                # old publish message, don't do anything
                return
        # update message to most recent
        self.clocks[clock_id] = clock
        # broadcast message to all channels
        await asyncio.gather(*(t.transmit(msg, context) for t in self.trxs))
