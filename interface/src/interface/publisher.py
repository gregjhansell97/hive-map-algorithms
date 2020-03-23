#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from interface.loggable import Loggable
from interface.transceiver import Transceiver


class Publisher(Loggable, ABC):
    """Responsible for publishing information (to a specific topic) using 
    transceivers provided

    Attributes:
        uid: identifier of object
        trxs: list of transceivers (used to broadcast)
    """

    def __init__(self, uid=None):
        super().__init__()
        if any(arg is None for arg in [uid]):
            raise TypeError("values cannot be none")
        self.uid = uid
        self.trxs = []

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.uid}"

    def use(self, trx: Transceiver):
        """Provide access to a transceiver that the publisher can use to 
        disperse its information

        Args:
            trx: transceiver used to broadcast information
        """
        self.trxs.append(trx)

    @abstractmethod
    async def publish(self, topic, data):
        """Publish raw data to a topic, ideally subscribers of the topic 
        receive this data

        Args:
            data: raw data being published
            topic: topic being published to
        """
        raise NotImplementedError
