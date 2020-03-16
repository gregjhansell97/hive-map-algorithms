#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import math

from transceivers.local_transceiver import LocalTransceiver

class EuclideanTransceiver(LocalTransceiver):
    """
    """

    def __init__(
            self, pos=(0, 0), tr_range=math.inf, recv_range=math.inf):
        super().__init__()
        self.pos = pos
        self.tr_range = tr_range
        self.recv_range = recv_range
        self.max_tr_range = tr_range
        self.max_recv_range = recv_range

    @property
    def transmit_strength(self):
        return self.tr_range/self.max_tr_range

    @transmit_strength.setter
    def transmit_strength(self, val):
        assert 0 <= val <= 1
        self.tr_range = val*self.max_tr_range

    @property
    def receive_strength(self):
        return self.recv_range/self.max_recv_range

    @receive_strength.setter
    def receive_strength(self, val):
        assert 0 <= val <= 1
        self.recv_range = val*self.max_recv_range

    def in_comm_range(self, t):
        """
        Checks if trx would be able to receive a transmission from self. The
        function is not commutative between self and trx

        Args:
            t(EuclideanTransceiver): transceiver checking range
        """
        pairwise_squared_error = ((v-u)**2 for v, u in zip(self.pos, t.pos))
        distance =  math.sqrt(sum(pairwise_squared_error))
        return distance < self.tr_range + t.recv_range


    async def transmit(self, data):
        """
        Gather receive method of all connections on every channel

        Args:
            data: data that connections will receive
        """
        # flattens connections
        connections = sum(self.channels, [])
        coros = (t.receive(data) for t in connections if self.in_comm_range(t))
        await asyncio.gather(*coros)
