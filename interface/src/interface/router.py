#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

from interface.transceiver import Transceiver


class Router(Transceiver.Callback):
    """
    Responsible for forwarding messages received by publisher to other
    subscribers and routers
    
    Attributes:
        id: identifier of object, its uniqueness is algorithm-dependent
        heartbeat_rate: interaction rate with other nodes
        routing_table_size: max size of routing table
        topic_priorities: list of topics of topics in prefered order
    """

    def __init__(
        self,
        id_: bytes,
        routing_table_size=math.inf,
        topic_priorities=[],
        heartbeat_rate=0.0,
    ):
        self.id = id_
        self.routing_table_size = routing_table_size
        self.topic_priorities = topic_priorities
        self.heartbeat_rate = heartbeat_rate
        self.trxs = []

    def use(self, trx: Transceiver):
        """
        Provide access to a transceiver that the subscriber can use to disperse
        and receive information about topics and routers

        Args:
            trx: transceiver used
        """
        trx.subscribe(self)
        self.trxs.append(trx)
