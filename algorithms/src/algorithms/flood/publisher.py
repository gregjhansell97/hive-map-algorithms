#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements publisher interface for network flooding algorithm
"""

import uuid

from pub_sub_interface import Publisher as ABCPublisher


class Publisher(ABCPublisher):
    """
    Implements ABCPublisher interface

    Attributes:
        id: unique identifier for the publisher
        clock: lamport clock where one event is a publish
    """

    def __init__(self, topic: int):
        super().__init__(uuid.uuid4().bytes, topic)
        self.clock = 0

    def publish(self, data):
        # id and time used to make unique message
        header = (self.id, self.clock, self.topic)
        msg = (header, data)
        self.clock += 1
        # self.trxs is from base class
        for t in self.trxs:
            t.transmit(msg)
