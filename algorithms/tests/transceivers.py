#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Transceivers and helper classes used for testing algorithms
"""

from pub_sub_interface.transceiver import Transceiver


class LocalTransceiver(Transceiver):
    """
    Interacts with other transceivers on the same thread. 
    LocalTransceiver is not thread-safe and is intended for testing purposes: 
    spoofing up interactions between subscribers, publishers, and routers. The
    connections are a chain of method invocations; this makes the class ideal
    for tests because it behaves consistently (with a followable stack trace)
    """

    def __init__(self):
        super().__init__()
        self.connections = []

    @staticmethod
    def connect(nodes=[], **kwargs):
        """
        Connect a list of components such that all components use transceiver
        that can communicate with one another

        Args:
            nodes: list of components to connect with one another
        """
        connections = LocalTransceiver.get_connections(len(nodes), **kwargs)
        # iterate through and have each node use a different transceiver
        for n, t in zip(nodes, connections):
            n.use(t)

    @staticmethod
    def get_connections(size: int):
        """
        Creates a fully connected network of local transceivers

        Args:
            size: desired number of transceivers in fully-connected-network

        Returns:
            (list): list of LocalSocket instances all interconnected
        """
        connections = [LocalTransceiver() for _ in range(size)]
        for t_i in connections:
            for t_j in connections:
                if t_i is not t_j:
                    t_i._connect(t_j)
        return connections

    @property
    def time(self):
        return 0

    def _connect(self, connection: Transceiver):
        """
        Connects one local transceiver to another. The connection is one-way.

        Args:
            connection: transceiver connecting to
        """
        self.connections.append(connection)

    def transmit(self, data):
        """
        Iterates through all connections and invokes their receive methods

        Args:
            data: data that connections will receive
        """
        for t in self.connections:
            t.receive(data)
