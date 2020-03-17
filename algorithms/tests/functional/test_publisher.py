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
    p = Publisher(5)
    await p.publish("hello world")

@pytest.mark.asyncio
async def test_publish_one_local_transceiver(algorithm):
    """
    Verify publish works with when using one tranceiver
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    t = LocalTransceiver()
    p.use(t)
    await p.publish("hello world")


@pytest.mark.asyncio
async def test_publish_many_transceivers(algorithm):
    """
    Verify publish works with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    await p.publish("goodbye yellow brick road")

@pytest.mark.asyncio
async def test_many_publish_many_transceivers(algorithm):
    """
    Verify publish works many times with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    await asyncio.gather(*(p.publish(i) for i in range(10)))
