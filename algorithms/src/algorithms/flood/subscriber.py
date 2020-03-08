#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements subscriber interface for network flooding algorithm
"""

from pub_sub_interface import Subscriber as ABCSubscriber
from pub_sub_interface import Transceiver


class Subscriber(ABCSubscriber):
    """
    Implements Subscriber interface

    Attributes:
        clocks(dict): tracks lamport times of messages received to determine if
            a message is stale
    """

    def __init__(self, topic: int, cb):
        super().__init__(topic, cb)
        self.clocks = {}

    def on_recv(self, trx: Transceiver, msg):
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
        self.callback(data)
