#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Facilitates receiving published messages of a certain topic. Subscriber part
of pub-sub paradigm of hive-map
"""

from abc import ABC, abstractmethod

from interface.loggable import Loggable
from interface.transceiver import Transceiver


class Subscriber(Loggable, ABC):
    """
    Responsible for invoking callbacks when messages of a certain topic are
    received

    Attributes:
        uid: identifier of object
        heartbeat_rate: cycles per second of node interations routine 
        callback: callback invoked on receiving message matching topic; it is a
            function that takes in one argument; this argument is the data
            published
        trxs: list of transceivers (used to broadcast and listen)
    """

    def __init__(self, topic=None, uid=None, callback=None, heartbeat_rate=0.0):
        super().__init__()
        if any(arg is None for arg in [uid, topic, callback]):
            raise TypeError("values cannot be none")
        self.uid = uid
        self.topic = topic
        self.callback = callback
        self.heartbeat_rate = heartbeat_rate
        self.trxs = []

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.uid}"

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
    async def on_recv(self, trx, data):
        raise NotImplementedError
