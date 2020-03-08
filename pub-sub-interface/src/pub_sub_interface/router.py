#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from pub_sub_interface.transceiver import Transceiver


class Router(ABC):
    """
    Responsible for forwarding messages received by publisher to other
    subscribers and routers
    
    Attributes:
        
    """

    def __init__(self):
        self.trxs = []

    def use(self, trx: Transceiver):
        """
        Provide access to a transceiver that the subscriber can use to disperse
        and receive information about topics and routers

        Args:
            trx: transceiver publs
        """
        trx._subscribe(self.on_recv)
        self.trxs.append(trx)

    @abstractmethod
    def on_recv(self, trx: Transceiver, time:int, msg):
        """
        Receives bytes of data at a certain time (this is the callback)

        Args:
            trx: transceiver that is invoking the callback
            time: time in user defined units
            msg: message being published
        """
        raise NotImplementedError
