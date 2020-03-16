#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

import pytest
import time

from benchmarks.transceivers import IPCTransceiver


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

def get_transceivers(num):
    b = IPCBroker()
    return (b, [b.create_transceiver() for _ in range(num)])

def start(objs):
    for o in objs:
        o.start()

def stop(objs):
    for o in objs:
        o.stop()

def get_trxs(num):
    return [IPCTransceiver() for _ in range(num)]
def test_ipc_initialization_start_stop():
    """
    Ensures transceiver can start and stop without crashing
    """
    trxs = get_trxs(4)
    IPCTransceiver.connect(trxs)
    # starts transceivers
    start(trxs)
    # kill transceivers
    stop(trxs)

def test_subscribe():
    """
    Ensures that subscribe method works as expected
    """
    trxs = get_trxs(1)
    start(trxs)
    cb = get_callback()
    trxs[0]._subscribe(cb)
    stop(trxs)

def test_transmit():
    """
    Verifies transmit method works as expected
    """
    trxs = get_trxs(1)
    start(trxs)
    trxs[0].transmit("one small step for man")
    stop(trxs)

def test_two_transceivers_communicate():
    trxs = get_trxs(2)
    IPCTransceiver.connect(trxs)
    cbs = [get_callback() for _ in range(2)]
    for t, cb in zip(trxs, cbs):
        t._subscribe(cb)
    start(trxs)
    trxs[0].transmit("one small step for man")
    trxs[1].transmit("one large leap for gerg")
    # messages must get to callback log in timely manner
    time.sleep(0.3)
    stop(trxs)

    assert cbs[0].log == [(trxs[0], "one large leap for gerg")]
    assert cbs[1].log == [(trxs[1], "one small step for man")]

def test_many_transceivers_communicate():
    num_trxs = 500
    trxs = get_trxs(num_trxs)
    IPCTransceiver.connect(trxs)
    cbs = [get_callback() for _ in range(num_trxs)]
    for t, cb in zip(trxs, cbs):
        t._subscribe(cb)
    start(trxs)
    for i in range(num_trxs):
        trxs[i].transmit(i)
    # messages must get to callback log in timely manner
    time.sleep(50)
    stop(trxs)
    for i in range(num_trxs):
        assert ( 
                set(cbs[i].log) == 
                {(trxs[i], j) for j in range(num_trxs) if j != i})

