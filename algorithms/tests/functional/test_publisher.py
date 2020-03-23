#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Publisher
"""

import asyncio
import pytest

from transceivers import LocalTransceiver

def test_initialization(algorithm):
    """
    Verify publisher can take in a topic and not crash
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(10)

@pytest.mark.asyncio
async def test_publish_no_transceiver(algorithm):
    """
    Verify publisher can publish even with no means of transceiver
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher("uid")
    await p.publish("topic", "msg")
    # verify logs
    assert p.logs[1] == [("published", "topic", "msg")]

@pytest.mark.asyncio
async def test_publish_one_local_transceiver(algorithm):
    """
    Verify publish works with when using one tranceiver
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher("uid")
    t = LocalTransceiver()
    p.use(t)
    await p.publish("topic", "msg")
    assert p.logs[1] == [("published", "topic", "msg")]


@pytest.mark.asyncio
async def test_publish_many_transceivers(algorithm):
    """
    Verify publish works with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher("uid")
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    await p.publish("topic", "msg")
    assert p.logs[1] == [("published", "topic", "msg")]

@pytest.mark.asyncio
async def test_many_publish_many_transceivers(algorithm):
    """
    Verify publish works many times with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher("uid")
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    # publish data
    num_pubs = 10 
    await asyncio.gather(*(p.publish("topic", i) for i in range(num_pubs)))
    assert (set(p.logs[1]) == 
            {("published", "topic", msg) for msg in range(num_pubs)})
