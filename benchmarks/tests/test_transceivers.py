#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""

from collections import defaultdict
from multiprocessing import Queue
import pytest

from ..transceivers import QTransceiver, distance


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

def get_transceiver(loc, radius):
    transmit_q = Queue()
    receive_q = Queue()
    t = QTransceiver(loc, radius, transmit_q, receive_q)
    t.start()
    return transmit_q, receive_q, t

def test_get_distance():
    """
    Verifies distance function calculates correct euclidian distance
    """
    assert distance((0, 0), (3, 4)) == 5
    assert distance((-1, -3), (2, 1)) == 5

def test_initialization_start_stop():
    """
    Ensures that Q transceivers can be started and stopped without crashing
    """
    transmit_q, receive_q, t = get_transceiver((0, 0), 10)
    t.stop()


def test_subscribe():
    """
    Ensures that subscribe method works as expected
    """
    transmit_q, receive_q, t = get_transceiver((0, 0), 10)
    t._subscribe(get_callback())
    t.stop()

def test_transmit():
    """
    Verifies transmit method works as expected
    """
    transmit_q, receive_q, t = get_transceiver((0, 0), 10)

    t.transmit("hello world")
    loc, r, data = transmit_q.get()
    assert loc == (0, 0)
    assert r == 10
    assert data == "hello world"
    t.stop()

def test_receive_transmission():
    """
    Behaves as expected when message is added to receive q
    """
    transmit_q, receive_q, t = get_transceiver((0, 0), 10)
    cb = get_callback()
    t._subscribe(cb)


    t.transmit("fingers crossed")
    receive_q.put(transmit_q.get())
    t.stop()
    assert cb.log == [(t, "fingers crossed")]

def test_receive_just_in_range_transmission():
    """
    Transmission message that was out of range
    """
    transmit_q_1, _, t_1 = get_transceiver((0, 0), 5)
    _, receive_q_2, t_2 = get_transceiver((3, 3.99), 1)

    cb = get_callback()
    t_2._subscribe(cb)

    t_1.transmit("hey")
    receive_q_2.put(transmit_q_1.get())
    t_1.stop()
    t_2.stop()
    assert cb.log == [(t_2, "hey")]
    
def test_receive_out_of_range_transmission():
    """
    Transmission message that was out of range
    """
    transmit_q_1, _, t_1 = get_transceiver((0, 0), 10)
    _, receive_q_2, t_2 = get_transceiver((20, 20), 10)

    cb = get_callback()
    t_2._subscribe(cb)

    t_1.transmit("hey")
    receive_q_2.put(transmit_q_1.get())
    t_1.stop()
    t_2.stop()
    assert cb.log == []
    
