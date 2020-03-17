#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements subscriber interface for network flooding algorithm
"""

import uuid

import interface
from interface import Transceiver


class Subscriber(interface.Subscriber):
    """
    Implements Subscriber interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine if
            a message is stale
    """

    def __init__(self, topic: int, cb, *args, **kwargs):
        super().__init__(uuid.uuid4().bytes, topic, cb, *args, **kwargs)
        self.clocks = {}

    async def on_recv(self, trx: Transceiver, msg, context):
        header, data = msg
        clock_id, clock, topic = header
        # not the right topic, subscriber doesn't care about it 
        if self.topic != topic:
            return
        # check for stale messages
        if clock_id in self.clocks:
            if clock <= self.clocks[clock_id]:
                return
        # update clock to most recent
        self.clocks[clock_id] = clock
        # invoke callback

        await self.callback(data)
