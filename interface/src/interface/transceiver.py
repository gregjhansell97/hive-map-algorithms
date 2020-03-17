#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import asyncio
import math


class Transceiver(ABC):
    """
    Layer below the network that transmits and receives messages from anonymous
    connections. Is a tool used by the main components: Publisher, Router and
    Subscriber

    Attributes:
        callbacks(list): list of coroutine callbacks
    """
    class Callback(ABC):
        async def relevant(self, context):
            return True
        async def invoke(self, trx, data, context): 
            # check context is relevant
            if await self.relevant(context):
                await self.on_recv(trx, data, context)
        @abstractmethod
        async def on_recv(self, trx, data, context):
            raise NotImplementedError

    def __init__(self):
        # callbacks have arguments (transceiver, data) in that order
        self.callbacks = []  # list of callbacks that get invoked on recv

    def __repr__(self):
        return f"{self.__class__.__name__}({id(self)})"

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
        raise NotImplementedError

    @transmit_strength.setter
    def transmit_strength(self, val):
        raise NotImplementedError

    @property
    def receive_strength(self):
        """
        Number from 0 to 1 that indicates the "range" of receiving information.
        """
        raise NotImplementedError

    @receive_strength.setter
    def receive_strength(self, val):
        raise NotImplementedError

    @property
    def time(self):
        """
        Current time check by the transceiver
        """
        raise NotImplementedError

    @abstractmethod
    async def transmit(self, data, context):
        """
        Bytes of data to send to all other reachable transceivers in the 
        network. This call is non-blocking. Must be implemented by subclasses.

        Args:
            data: information being transmitted to all other transceivers
            context: circumstances of data transmission

        Raises:
            BufferError: when message cannot be sent or buffered
        """
        raise NotImplementedError

    async def receive(self, data, context):
        """
        Invoked by child class to deliver messages received to transceiver. Acts 
        as the original event driver

        Args:
            data: information being received
            context: circumstances of data transmission
        """
        # gather callbacks and run them
        invocations = (cb.invoke(self, data, context) for cb in self.callbacks)
        await asyncio.gather(*invocations)

    def subscribe(self, cb: Callback):
        """
        Subscribes a callback that receives messages that the transceiver
        receives
        
        Args:
            cb: callback invoked when data is received
        """
        self.callbacks.append(cb)
