#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests pub-sub network without routers involved, mostly analyzes the interaction
between subscribers and publishers
"""

import asyncio
import pytest

from tests.functional.helpers import get_callback
from tests.system.helpers import TOPIC, DIFF_TOPIC, connect

@pytest.mark.asyncio
async def test_one_pub_one_sub_one_local_connection(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them
    over the same topic and confirm that messages get sent 
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(TOPIC)
    s = Subscriber(TOPIC, get_callback())
    # connect components
    connect([p, s])
    # confirm simple publishes work
    await asyncio.gather(*(p.publish(i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))

@pytest.mark.asyncio
async def test_one_pub_one_sub_many_local_connections(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them
    with multiple transceivers and verify that the message only gets delivered
    once... is that a property we want to enforce to some capacity?
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(TOPIC)
    s = Subscriber(TOPIC, get_callback())
    # connect components
    for i in range(10):
        connect([p, s])
    # confirm simple publishes work 
    await p.publish("msg1")
    assert s.callback.log == ["msg1"]
    await p.publish("msg2")
    assert s.callback.log == ["msg1", "msg2"]
    # clear log
    s.callback.log = []
    await asyncio.gather(*(p.publish(i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))


@pytest.mark.asyncio
async def test_one_pub_many_sub_local_connections(algorithm):
    """
    Get one publisher instance and many subscribers and verify that the 
    messages are published to all subscribers
    """
    Publisher, Subscriber, Router = algorithm
    # publishers
    p = Publisher(TOPIC)
    # subscribers
    num_subs = 10
    subs = [Subscriber(TOPIC, get_callback()) for _ in range(num_subs)]
    diff_subs = [
            Subscriber(DIFF_TOPIC, get_callback()) for _ in range(num_subs)
    ]
    # connect components
    connect([p] + subs + diff_subs)
    # verification
    await p.publish(1)
    assert all([s.callback.log == [1] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])
    await p.publish(2)
    assert all([s.callback.log == [1, 2] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])

@pytest.mark.asyncio
async def test_many_pub_one_sub_local_connections(algorithm):
    """
    Get many publisher instances and many subscribers and verify that the 
    messages are published to the subscriber
    """
    Publisher, Subscriber, Router = algorithm
    # publishers
    num_pubs = 10
    pubs = [Publisher(TOPIC) for _ in range(num_pubs)]
    diff_pubs = [Publisher(DIFF_TOPIC) for _ in range(num_pubs)]
    # subscribers
    sub = Subscriber(TOPIC, get_callback())
    # connect components
    connect([sub] + pubs + diff_pubs)
    # verification
    expected_log = []
    await pubs[0].publish(0)
    assert sub.callback.log == [0]
    # other topic, subscriber should not be interested
    await asyncio.gather(*(p.publish("no msg") for p in diff_pubs))
    assert sub.callback.log == [0]
    # clear log
    sub.callback.log = []
    # subscriber should be interested
    transmissions = (p.publish(i) for p, i in zip(pubs, range(len(pubs))))
    await asyncio.gather(*transmissions)
    assert set(sub.callback.log) == set(range(len(pubs)))


@pytest.mark.asyncio
async def test_many_pub_many_sub_local_connections(algorithm):
    """
    Get many publisher instances and many subscribers and verify that the 
    messages are published to all subscribers
    """
    Publisher, Subscriber, Router = algorithm
    # publishers
    num_pubs = 10
    pubs = [Publisher(TOPIC) for _ in range(num_pubs)]
    diff_pubs = [Publisher(DIFF_TOPIC) for _ in range(num_pubs)]
    # subscribers
    num_subs = 10
    subs = [Subscriber(TOPIC, get_callback()) for _ in range(num_subs)]
    diff_subs = [Subscriber(DIFF_TOPIC, get_callback()) for _ in subs]
    # connect components
    connect(pubs + diff_pubs + subs + diff_subs)
    # verify
    await pubs[0].publish(0)
    assert all([s.callback.log == [0] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])
    # clear logs
    for s in subs:
        s.callback.log = []
    await asyncio.gather(*(p.publish(id(p)) for p in pubs + diff_pubs))    
    pub_ids = {id(p) for p in pubs} 
    diff_pub_ids = {id(p) for p in diff_pubs} 
    assert all([set(s.callback.log) == pub_ids for s in subs])
    assert all([set(s.callback.log) == diff_pub_ids for s in diff_subs])
