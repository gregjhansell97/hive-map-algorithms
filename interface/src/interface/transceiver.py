#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import asyncio
import math
import time

from interface.loggable import Loggable


class Transceiver(Loggable, ABC):
    """
    Layer below the network that transmits and receives messages from anonymous
    connections. Is a tool used by the main components: Publisher, Router and
    Subscriber

    Attributes:
        callbacks(list): list of coroutine callbacks
    """

    def __init__(self):
        # callbacks have arguments (transceiver, data) in that order
        super().__init__()
        self.callbacks = []  # list of callbacks

    def __str__(self):
        return f"{id(self)}"

    def __repr__(self):
        return str(self)

    @property
    def max_msg_size(self):
        """
        Largest possible message size for data. For benchmarks this size is
        infinite, but I wanted to acknowledge it for the actual implementation
        """
        return math.inf

    @property
    def transmit_strength(self):
        """
        Number from 0 to 1 that indicates the "range" of the transmission.
        """
        return 1

    @transmit_strength.setter
    def transmit_strength(self, val):
        raise NotImplementedError

    @property
    def receive_strength(self):
        """
        Number from 0 to 1 that indicates the "range" of receiving information.
        """
        return 1

    @receive_strength.setter
    def receive_strength(self, val):
        raise NotImplementedError

    @property
    def time(self):
        """
        Current time check by the transceiver
        """
        return time.process_time()

    @abstractmethod
    async def transmit(self, data):
        """
        Bytes of data to send to all other reachable transceivers in the 
        network. This call is non-blocking. Must be implemented by subclasses.

        Args:
            data: information being transmitted to all other transceivers

        Raises:
            BufferError: when message cannot be sent or buffered
        """
        raise NotImplementedError

    async def receive(self, data):
        """
        Invoked by child class to deliver messages received to transceiver. Acts 
        as the original event driver

        Args:
            data: information being received
        """
        # gather callbacks and run them
        invocations = (cb(self, data) for cb in self.callbacks)
        await asyncio.gather(*invocations)

    def subscribe(self, cb):
        """
        Subscribes a callback that receives messages that the transceiver
        receives
        
        Args:
            cb: callback invoked when data is received
        """
        self.callbacks.append(cb)
