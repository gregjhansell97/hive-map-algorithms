#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements router interface for network flooding algorithm
"""

from pub_sub_interface import Router as ABCRouter
from pub_sub_interface import Transceiver


class Router(ABCRouter):
    """
    Implements Router interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine
            if a message is stale
    """

    def __init__(self):
        super().__init__()
        self.clocks = {}

    def on_recv(self, trx: Transceiver, msg):
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
        for t in self.trxs:
            t.transmit(msg)
