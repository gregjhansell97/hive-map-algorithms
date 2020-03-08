#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class Transceiver(ABC):
    """
    Layer below the network that transmits and receives messages from anonymous
    connections. Is a tool used by the main components: Publisher, Router and
    Subscriber
    """

    def __init__(self):
        # callbacks have arguments (transceiver, data) in that order
        self._callbacks = []  # list of callbacks that get invoked on recv

    @abstractmethod
    def transmit(self, data):
        """
        Bytes of data to send to all other reachable transceivers in the 
        network. This call is non-blocking. Must be implemented by subclasses

        Args:
            data: raw bytes being transmitted to all other transceivers
        """
        raise NotImplementedError

    def receive(self, time, data):
        """
        Invoked by child class to deliver messages received to transceiver. Acts 
        as the original event driver

        Args:
            time: time that message was received
            data: raw bytes del
        """
        for cb in self._callbacks:
            cb(self, time, data)

    def _subscribe(self, cb):
        """
        Subscribes a callback that receives messages that the transceiver
        receives
        
        Args:
            cb: callback invoked when data is received
        """
        self._callbacks.append(cb)
