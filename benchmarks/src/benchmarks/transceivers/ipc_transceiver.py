#!/usr/bin/
# -*- coding: utf-8 -*-

from multiprocessing import Process, Queue
from threading import Thread
import uuid

from pub_sub_interface.transceiver import Transceiver

class IPCTransceiver(Transceiver):
    def __init__(self, transmitter=None, transmission=None):
        super().__init__()
        self.uid = str(uuid.uuid4())
        self.transmitters = []
        self.transmission = Queue()
        # attach thread data
        self.transmission.thread = Thread(target=self.listen)
    @staticmethod
    def connect(trxs):
        #NOTE all connections must be made before starting transceivers
        assert not any([t.transmission.thread.is_alive() for t in trxs])
        transmission = Queue()
        # attaching meta information
        for t in trxs:
            t.transmitters.append(transmission)
        # listen will run on a daemon process
        def listen(transmission, transmitters):
            while True:
                # waits for transmission
                item = transmission.get()
                if item == None:
                    break
                uid, data = item 
                for t in transmitters:
                    t.put(item)
        daemon_process = Process(
                target=listen,
                args=(transmission, [t.transmission for t in trxs]),
                daemon=True)
        daemon_process.start()
        return daemon_process
    @property
    def receive_strength(self):
        raise NotImplementedError
    @receive_strength.setter
    def receive_strength(self, val):
        raise NotImplementedError
    @property
    def transmit_strength(self):
        raise NotImplementedError
    @transmit_strength.setter
    def transmit_strength(self, val):
        raise NotImplementedError
    @property
    def time(self):
        raise NotImplementedError
    def start(self):
        self.transmission.thread.start()
    def stop(self):
        for t in self.transmitters:
            t.put(None) # poison pill
        self.transmission.put(None)
        self.transmission.thread.join()
    def listen(self):
        while True:
            # waits for transmission
            item = self.transmission.get()
            if item == None:
                break
            uid, data = item
            # don't deliver to self
            if uid == self.uid:
                continue
            self.receive(data)
    def transmit(self, data):
        for t in self.transmitters:
            t.put((self.uid, data))
