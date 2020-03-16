#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import math

from interface.transceiver import Transceiver


class LocalTransceiver(Transceiver):
    """
    """

    def __init__(self):
        super().__init__()
        self.channels = []

    @classmethod
    def connect(cls, trxs):
        """
        Connect a list of transceivers such that all transceivers can
        communicate with one another, each connection list is a 'channel'

        Args:
            trxs: list of transceivers to connect with one another
        """
        for t in trxs:
            # transceiver, t, is connected to everything but itself
            connections = [c for c in trxs if c is not t]
            t.channels.append(connections)

    async def transmit(self, data):
        """
        Gather receive method of all connections on every channel

        Args:
            data: data that connections will receive
        """
        # flattens connections
        connections = sum(self.channels, [])
        await asyncio.gather(*(t.receive(data) for t in connections))
