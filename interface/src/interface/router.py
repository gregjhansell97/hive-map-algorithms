#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import math

from interface.loggable import Loggable
from interface.transceiver import Transceiver


class Router(Loggable, ABC):
    """
    Responsible for forwarding messages received by publisher to other
    subscribers and routers
    
    Attributes:
        uid: identifier of object
        heartbeat_rate: interaction rate with other nodes (cycles per second)
        routing_table_size: max number of items router can store
        topic_preferences: list of topics in prefered order
    """

    def __init__(
        self,
        uid=None,
        routing_table_size=math.inf,
        topic_preferences=[],
        heartbeat_rate=0.0,
    ):
        super().__init__()
        if any(arg is None for arg in [uid]):
            raise TypeError("args cannot be none")
        self.uid = uid
        self.routing_table_size = routing_table_size
        self.heartbeat_rate = heartbeat_rate
        self.topic_preferences = topic_preferences
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
            trx: transceiver used
        """
        trx.subscribe(self.on_recv)
        self.trxs.append(trx)

    @abstractmethod
    async def on_recv(self, trx, data):
        raise NotImplementedError
