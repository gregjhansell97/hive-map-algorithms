#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for LocalSocket; the main target of these tests is AbstractSocket
"""
import asyncio
import pytest
import random as rand

from tests.helpers import get_callback

def test_in_comm_range(ET):
    t1 = ET(pos=(0, 0), tr_range=5, recv_range=1)
    t2 = ET(pos=(3, 4), tr_range=2, recv_range=1)
    assert t1.in_comm_range(t2)
    assert not t2.in_comm_range(t1)
    t1.pos = (3, 6) # move t1 closer to t2
    assert t1.in_comm_range(t2)
    assert t2.in_comm_range(t1)
    t2.pos = (-100, -100) # move t2 really far away
    assert not t1.in_comm_range(t2)
    assert not t2.in_comm_range(t1)
    t1.pos = (-100, -99) # get close to t2
    assert t1.in_comm_range(t2)
    assert t2.in_comm_range(t1)
    t1.pos = (-100, -100) # get really close to t2
    assert t1.in_comm_range(t2)
    assert t2.in_comm_range(t1)

def test_range_adjustment(ET):
    t1 = ET(pos=(0, 0), tr_range=5, recv_range=1)
    t2 = ET(pos=(3, 4), tr_range=2, recv_range=1)
    assert t1.transmit_strength == 1
    assert t1.receive_strength == 1
    t1.transmit_strength = 0.5
    assert t1.transmit_strength == 0.5
    assert t1.receive_strength == 1
    assert not t1.in_comm_range(t2)
    assert not t2.in_comm_range(t1)
    t1.transmit_strength = 0.85
    assert t1.in_comm_range(t2)
    assert not t2.in_comm_range(t1)
    t2.receive_strength = 0
    assert t2.transmit_strength == 1
    assert t2.receive_strength == 0
    assert not t1.in_comm_range(t2)
    assert not t2.in_comm_range(t1)

@pytest.mark.asyncio
async def test_connections(ET):
    """
    Ensures that communication restricted to transcievers in range
    """
    # create connections
    trxs = [
            ET(pos=(0, 0), tr_range=5, recv_range=2),
            ET(pos=(3, 4), tr_range=2, recv_range=1),
            ET(pos=(3, 3), tr_range=1.5, recv_range=0),
            ET(pos=(100, -100), tr_range=3, recv_range=3)
    ]
    ET.connect(trxs)
    # subscribe each transceiver to a callback
    for t in trxs:
        t.subscribe(get_callback())
    # extract transceivers from list
    # t1 can talk to t2, t3
    # t2 can talk to t3
    # t3 can talk to t2
    # t4 can talk to no one
    [t1, t2, t3, t4] = trxs

    transmissions = [
        t1.transmit("t1 message"),
        t2.transmit("t2 message"),
        t3.transmit("t3 message"),
        t4.transmit("t4 message")
    ]
    # extract callbacks for transceivers
    [c1, c2, c3, c4] = [t.callbacks[0] for t in trxs]
    await asyncio.gather(*transmissions)
    assert len(c1.log) == 0 # no messages could be received
    assert set(c2.log) == {(t2, "t1 message"), (t2, "t3 message")}
    assert set(c3.log) == {(t3, "t1 message"), (t3, "t2 message")}
    assert len(c4.log) == 0 # no messages could be received

@pytest.mark.asyncio
async def test_large_scale_communication_network(ET):
    num_transceivers = 1000
    rand.seed(9694) # makes the results reproducable 
    min_y = min_x = -100
    max_y = max_x = 100
    max_range = 10
    # create connections
    trxs = []
    for _ in range(num_transceivers):
        x = rand.uniform(min_x, max_x)
        y = rand.uniform(min_y, max_y)
        tr_range = rand.uniform(0, max_range)
        recv_range = rand.uniform(0, max_range)
        trxs.append(ET(pos=(x, y), tr_range=tr_range, recv_range=recv_range))
    ET.connect(trxs)
    # subscribe each transceiver to a callback
    for t in trxs:
        t.subscribe(get_callback())
    # publish messages
    transmissions = [t.transmit(id(t)) for t in trxs]
    await asyncio.gather(*transmissions)
    # make all callback logs sets (to speed up access)
    for t in trxs:
        t.callbacks[0].log = set(t.callbacks[0].log)
    # verify messages received
    for t1 in trxs:
        for t2 in trxs:
            if t1 is not t2 and t1.in_comm_range(t2):
                assert (t2, id(t1)) in t2.callbacks[0].log






