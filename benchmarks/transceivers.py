#!/usr/bin/
# -*- coding: utf-8 -*-

import math
from multiprocessing import Process, Queue
from threading import Thread
import time
import uuid

import zmq

from pub_sub_interface.transceiver import Transceiver

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class IPCBroker:
    class IPCTransceiver(Transceiver): 

class IPCBroker:
    """
    start, and stop: create process that handles messages
    """
    def __init__(self, channel:str, context=None):
        if context is None:
            context = zmq.Context()
        self.context = context
        self.channel = channel
        self.listen_process = Process(target=self.listen)

    def start(self):
        self.listen_process.start()

    def stop(self):
        ender = self.context.socket(zmq.PUSH)
        ender.connect(f"ipc://./.tr-{self.channel}.ipc")
        ender.send_pyobj(None) # any non-standard message ends listen process
        self.listen_process.join()


    def listen(self):
        context = zmq.Context()
        # create transmission
        transmission = context.socket(zmq.PULL)
        transmission.bind(f"ipc://./.tr-{self.channel}.ipc")
        # create publisher
        publisher = context.socket(zmq.PUB)
        publisher.bind(f"ipc://./.rcv-{self.channel}.ipc")
        # loop and listen for incoming message
        while True:
            item = transmission.recv_pyobj()
            print(item)
            if item is None:
                break
            trx_id, data = item
            time.sleep(0.2)
            publisher.send_pyobj((trx_id, data))



class IPCTransceiver(Transceiver):
    def __init__(self, channel:str, context=None):
        super().__init__()
        if context is None:
            context = zmq.Context()
        self.context = context
        self.channel = channel
        self.uid = str(uuid.uuid4()) # unique id in a pinch!
        # create the transmitter
        self.transmitter = context.socket(zmq.PUSH)
        # linger ensures context can close with message queued
        self.transmitter.setsockopt(zmq.LINGER, 0)
        self.transmitter.connect(f"ipc://./.tr-{self.channel}.ipc")
        # create request socket that will stop the listener thread
        self.ender = context.socket(zmq.REQ) # will connect when thread id known
        self.receiver_thread = Thread(target=self.listen)

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
        self.receiver_thread.start()
        self.ender.connect(f"inproc://{self.uid}")

    def stop(self):
        # ender sends message to poison pill in listen thread
        self.ender.send_pyobj(None)
        self.receiver_thread.join()

    def listen(self):
        # bind poison pill
        poison_pill = self.context.socket(zmq.REP)
        poison_pill.bind(f"inproc://{self.uid}")
        # connect receiver
        receiver = self.context.socket(zmq.SUB)
        receiver.setsockopt(zmq.SUBSCRIBE, b"")
        receiver.connect(f"ipc://./.rcv-{self.channel}.ipc")
        # create poller that waits for receiver or poison pill
        poller = zmq.Poller()
        poller.register(receiver, zmq.POLLIN)
        poller.register(poison_pill, zmq.POLLIN)
        while True:
            socks = dict(poller.poll())
            if poison_pill in socks and socks[poison_pill] == zmq.POLLIN:
                # poison pill sent a message... end thread
                break
            elif receiver in socks and socks[receiver] == zmq.POLLIN:
                uid, data = receiver.recv_pyobj()
                if uid != self.uid:
                    self.receive(data)
    
    def transmit(self, data):
        self.transmitter.send_pyobj((self.uid, data))


class EuclideanTransceiver(IPCTransceiver):
    pass
