#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements publisher interface for network flooding algorithm
"""

import asyncio
import uuid

from interface import Publisher as ABCPublisher


class Publisher(ABCPublisher):
    """
    Implements ABCPublisher interface

    Attributes:
        id: unique identifier for the publisher
        clock: lamport clock where one event is a publish
    """

    def __init__(self, topic: int, *args, **kwargs):
        super().__init__(uuid.uuid4().bytes, topic, *args, **kwargs)
        self.clock = 0

    async def publish(self, data):
        # id and time used to make unique message
        header = (self.id, self.clock, self.topic)
        msg = (header, data)
        self.clock += 1
        # transmit over all transmitters
        await asyncio.gather(*(t.transmit(msg) for t in self.trxs))
