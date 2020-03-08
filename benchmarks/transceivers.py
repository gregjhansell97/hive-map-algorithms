#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pub_sub_interface.transceiver import Transceiver

class IPCTransceiver(Transceiver):
    """
    Communication from one processes to another based on location and radius,
    if a process is within a certain radius away it will receive the message
    otherwise it will not. Runs a background thread that waits for received
    messages. IT MUST HAVE A TRANSCEIVER DELEGATE TO WORK
    """

    def __init__(self, loc, radius, transmit_q, receive_q):
        super().__init__()
        self.loc = loc
        self.radius = radius
        self.transmit_q = transmit_q
        self.receive_q = receive_q

    def listen(self):
        """
        Loops on a separate thread for messages
        """
        try:
            while True:
                loc, r, data = self.receive_q.get()
                if distance(loc, self.loc) < r:
                    self.receive(None, data) 
        except TypeError: # poison pill
            pass


    def transmit(self, data):
        """
        Iterates through all connections and invokes their receive methods

        Args:
            data: information that connections will receive
        """
        self.transmit_q.put(self.loc, self.radius, data)
