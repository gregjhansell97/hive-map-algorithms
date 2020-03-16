#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Facilitates receiving published messages of a certain topic. Subscriber part
of pub-sub paradigm of hive-map
"""

from abc import ABC, abstractmethod

from interface.transceiver import Transceiver


class Subscriber(ABC):
    """
    Responsible for invoking callbacks when messages of a certain topic are
    received

    Attributes:
        id: identifier of object, its uniqueness is algorithm-dependent
        topic: topic of interest for subscriber
        heartbeat_rate: interaction rate with other nodes
        callback: callback invoked on receiving message matching topic; it is a
            function that takes in one argument; this argument is the data
            published
            trxs: list of transceivers (used to broadcast and listen)
    """

    def __init__(self, id_: bytes, topic: int, cb=None, heartbeat_rate=0.0):
        self.id = id_
        self.topic = topic
        self.heartbeat_rate = heartbeat_rate
        self.callback = cb
        self.trxs = []

    def use(self, trx: Transceiver):
        """
        Provide access to a transceiver that the subscriber can use to disperse
        and receive information about topics and routers

        Args:
            trx: transceiver about to be used
        """
        trx.subscribe(self.on_recv)
        self.trxs.append(trx)

    @abstractmethod
    async def on_recv(self, trx: Transceiver, data):
        """
        Receives bytes of data at a certain time (this is the callback)

        Args:
            trx: transceiver that is invoking the callback
            time: time in user defined units
            data: data being received
        """
        raise NotImplementedError
