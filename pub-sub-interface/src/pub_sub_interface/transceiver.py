#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import math


class Transceiver(ABC):
    """
    Layer below the network that transmits and receives messages from anonymous
    connections. Is a tool used by the main components: Publisher, Router and
    Subscriber
    """

    def __init__(self):
        # callbacks have arguments (transceiver, data) in that order
        self._callbacks = []  # list of callbacks that get invoked on recv

    @property
    def max_msg_size(self):
        """
        Largest possible message size for data. For benchmarks this size is
        infinite, but I wanted to acknowledge it for the actual implementation
        """
        return math.inf

    @property
    @abstractmethod
    def transmit_strength(self):
        """
        Number from 0 to 1 that indicates the "range" of the transmission.
        """
        raise NotImplementedError

    @transmit_strength.setter
    @abstractmethod
    def transmit_strength(self, val):
        raise NotImplementedError


    @property
    @abstractmethod
    def receive_strength(self):
        """
        Number from 0 to 1 that indicates the "range" of receiving information.
        """
        raise NotImplementedError

    @transmit_strength.setter
    @abstractmethod
    def receive_strength(self, val):
        raise NotImplementedError


    @property
    @abstractmethod
    def time(self):
        """
        Current time check by the transceiver
        """
        raise NotImplementedError

    def transmit(self, data):
        """
        Bytes of data to send to all other reachable transceivers in the 
        network. This call is non-blocking. Must be implemented by subclasses.

        Args:
            data: information being transmitted to all other transceivers

        Raises:
            BufferError: when message cannot be sent or buffered
        """
        raise NotImplementedError

    def receive(self, data):
        """
        Invoked by child class to deliver messages received to transceiver. Acts 
        as the original event driver

        Args:
            data: information being received
        """
        for cb in self._callbacks:
            cb(self, data)

    def _subscribe(self, cb):
        """
        Subscribes a callback that receives messages that the transceiver
        receives
        
        Args:
            cb: callback invoked when data is received
        """
        self._callbacks.append(cb)
