#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
import logging
import asyncio
import pytest

from tests.helpers import get_callback

@pytest.mark.asyncio
async def test_connections(LT):
    """
    Ensures that local transceivers can be connected
    """
    # parameters
    num_connections = 10
    num_callbacks = 5
    # create connections
    trxs = [LT() for _ in range(num_connections)]
    LT.connect(trxs)
    [t, *_] = trxs
    # subscribe to callbacks
    for _ in range(num_callbacks):
        t.subscribe(get_callback())
    assert len(t.callbacks) == num_callbacks
    await t.transmit("no message")
    await trxs[3].transmit("message from 3")
    for cb in t.callbacks:
        assert cb.log == [(t, "message from 3")]

@pytest.mark.asyncio
async def test_full_interaction(LT):
    """
    Ensures complete communication between many (100) transceivers
    """
    # parameters
    num_connections = 100
    num_callbacks = 3
    # create connections
    trxs = [LT() for _ in range(num_connections)]
    LT.connect(trxs)
    # subscribe each transceiver to a callback
    for t in trxs:
        t.subscribe(get_callback())
    # have each transceiver publish messages and gather them
    transmissions = []
    for t in trxs:
        transmissions.append(t.transmit(id(t)))
    await asyncio.gather(*transmissions)
    ids = {id(t) for t in trxs}
    # make all callback logs sets (to speed up access)
    for t in trxs:
        t.callbacks[0].log = set(t.callbacks[0].log)
    # check that all messages made it through 
    for t1 in trxs:
        for t2 in trxs:
            if t1 is not t2:
                assert (t2, id(t1)) in t2.callbacks[0].log
        
