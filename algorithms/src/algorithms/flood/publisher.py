#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements publisher interface for network flooding algorithm
"""

import asyncio

import interface


class Publisher(interface.Publisher):
    """
    Implements ABCPublisher interface

    Attributes:
        id: unique identifier for the publisher
        clock: lamport clock where one event is a publish
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clock = 0

    async def publish(self, topic, data):
        # uid and time used to make unique message
        header = (self.uid, self.clock, topic)
        msg = (header, data)
        self.clock += 1
        # transmit over all transmitters
        await self.log(("published", topic, data))
        await asyncio.gather(*(t.transmit(msg) for t in self.trxs))
