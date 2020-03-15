#!/usr/bin/
# -*- coding: utf-8 -*-

import math
from threading import Thread

from pub_sub_interface.transceiver import Transceiver

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class QTransceiver(Transceiver):
    """
    Communication from one proceses to another over queues. All outgoing
    messages are placed on a queue and so are incoming messages. A transceiver
    has a location on a 2-d map and a radius of communication
    """

    def __init__(self, loc, radius, transmit_q, receive_q):
        super().__init__()
        self.loc = loc
        self.radius = radius
        self.transmit_q = transmit_q
        self.receive_q = receive_q
        self.listen_thread = Thread(target=self.listen)

    @property
    def receive_strength(self):
        return 1.0

    @receive_strength.setter
    def receive_strength(self, val):
        raise NotImplementedError

    @property
    def transmit_strength(self):
        return 1.0

    @transmit_strength.setter
    def transmit_strength(self, val):
        raise NotImplementedError

    @property
    def time(self):
        return 0

    def start(self):
        self.listen_thread.start()

    def stop(self):
        self.receive_q.put(None)
        self.listen_thread.join()

    def listen(self):
        """
        Loops on a separate thread for messages
        """
        try:
            while True:
                loc, r, data = self.receive_q.get()
                if distance(loc, self.loc) < r:
                    self.receive(data) 
        except TypeError: # poison pill
            # clear out remainder of receives (while not empty)
            # end process
            pass


    def transmit(self, data):
        """
        Iterates through all connections and invokes their receive methods

        Args:
            data: information that connections will receive
        """
        self.transmit_q.put((self.loc, self.radius, data))
