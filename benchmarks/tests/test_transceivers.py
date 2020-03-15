#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
from multiprocessing import Queue
import pytest
import time

from ..transceivers import IPCTransceiver, IPCBroker


def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """

    def cb(trx, data):
        # callbacks for transceivers expects a transceiver instance, a time,
        # and data
        cb.log.append((trx, data))

    cb.log = []  # log tracks the data received and by which transceiver
    return cb

def test_ipc_initialization_start_stop():
    """
    Ensures that ipc queue can start and stop without crashing or hanging
    """
    # checks the broker
    b = IPCBroker("ipc_initialization")
    # checks transceiver
    t = IPCTransceiver(b.channel, context=b.context)

    # starts them both up
    t.start()
    b.start()
    # kill them both
    t.stop()
    b.stop()

def test_subscribe():
    """
    Ensures that subscribe method works as expected
    """
    t = IPCTransceiver("test_subscriber")
    t.start()
    cb = get_callback()
    t._subscribe(cb)
    t.stop()

def test_transmit():
    """
    Verifies transmit method works as expected
    """
    t = IPCTransceiver("test_transmit")
    t.start()
    t.transmit("one small step for man")
    t.stop()

def test_two_transceivers_communicate():
    b = IPCBroker("test_two_transceivers_communicate")
    t_1 = IPCTransceiver(b.channel, context=b.context)
    t_2 = IPCTransceiver(b.channel, context=b.context)
    # track callbacks
    cb_1 = get_callback()
    t_1._subscribe(cb_1)
    cb_2 = get_callback()
    t_2._subscribe(cb_2)

    # start components
    t_1.start()
    t_2.start()
    b.start()
    # slow joiners syndrom!!!
    time.sleep(0.2)
    t_1.transmit("one small step for man")
    t_2.transmit("one large leap for gerg")
    time.sleep(0.2) # wait for stuff to happen

    t_1.stop()
    t_2.stop()
    b.stop()

    print(cb_1.log)
    print(cb_2.log)

    assert cb_1.log == [(t_1, "one large leap for gerg")]
    assert cb_2.log == [(t_2, "one small step for man")]


def test_receive_just_in_range_transmission():
    """
    Transmission message that was out of range
    """
    pass
    
def test_receive_out_of_range_transmission():
    """
    Transmission message that was out of range
    """
    pass
    
