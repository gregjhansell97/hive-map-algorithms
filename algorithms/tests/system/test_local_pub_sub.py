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
    # initialization
    p = Publisher(uid="p-id")
    s = Subscriber(uid="s-id", topic=TOPIC, callback=get_callback())
    # connect components
    connect([p, s])
    # confirm simple publishes work
    await asyncio.gather(*(p.publish(TOPIC, i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))

@pytest.mark.asyncio
async def test_one_pub_one_sub_many_local_connections(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them
    with multiple transceivers and verify that the message only gets delivered
    once... is that a property we want to enforce to some capacity?
    """
    Publisher, Subscriber, Router = algorithm
    # initialization
    p = Publisher(uid="p-id")
    s = Subscriber(uid="s-id", topic=TOPIC, callback=get_callback())
    # connect components
    for i in range(10):
        connect([p, s])
    # confirm simple publishes work 
    await p.publish(TOPIC, "msg1")
    assert s.callback.log == ["msg1"]
    await p.publish(TOPIC, "msg2")
    await p.publish(DIFF_TOPIC, "msg3")
    assert s.callback.log == ["msg1", "msg2"]
    # clear log
    s.callback.log = []
    await asyncio.gather(*(p.publish(TOPIC, i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))


@pytest.mark.asyncio
async def test_one_pub_many_sub_local_connections(algorithm):
    """
    Get one publisher instance and many subscribers and verify that the 
    messages are published to all subscribers
    """
    Publisher, Subscriber, Router = algorithm
    # publishers
    p = Publisher(uid="p-id")
    # subscribers
    num_subs = 10
    subs = [
            Subscriber(uid=f"{i}", topic=TOPIC, callback=get_callback()) 
            for i in range(num_subs)
    ]
    diff_subs = [
            Subscriber(uid=f"d{i}", topic=DIFF_TOPIC, callback=get_callback()) 
            for i in range(num_subs)
    ]
    # connect components
    connect([p] + subs + diff_subs)
    # verification
    await p.publish(TOPIC, 1)
    assert all([s.callback.log == [1] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])
    await p.publish(TOPIC, 2)
    assert all([s.callback.log == [1, 2] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])
    await p.publish(DIFF_TOPIC, 3)
    assert all([s.callback.log == [1, 2] for s in subs])
    assert all([s.callback.log == [3] for s in diff_subs])

@pytest.mark.asyncio
async def test_many_pub_one_sub_local_connections(algorithm):
    """
    Get many publisher instances and many subscribers and verify that the 
    messages are published to the subscriber
    """
    Publisher, Subscriber, Router = algorithm
    # publishers
    num_pubs = 10
    pubs = [Publisher(uid=f"p{i}") for i in range(num_pubs)]
    # subscribers
    sub = Subscriber(uid="s", topic=TOPIC, callback=get_callback())
    # connect components
    connect([sub] + pubs)
    # verification
    expected_log = []
    await pubs[0].publish(TOPIC, 0)
    assert sub.callback.log == [0]
    # other topic, subscriber should not be interested
    await asyncio.gather(*(p.publish(DIFF_TOPIC, "no msg") for p in pubs))
    assert sub.callback.log == [0]
    # clear log
    sub.callback.log = []
    # subscriber should be interested
    transmissions = (p.publish(TOPIC, i) for p, i in zip(pubs, range(len(pubs))))
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
    pubs = [Publisher(uid=f"P{i}") for i in range(num_pubs)]
    # subscribers
    num_subs = 10
    subs = [
            Subscriber(uid=f"S{i}", topic=TOPIC, callback=get_callback()) 
            for i in range(num_subs)
    ]
    diff_subs = [
            Subscriber(uid=f"DS{i}", topic=DIFF_TOPIC, callback=get_callback()) 
            for i in range(num_subs)
    ]
    # connect components
    connect(pubs + subs + diff_subs)
    # verify
    await pubs[0].publish(TOPIC, 0)
    assert all([s.callback.log == [0] for s in subs])
    assert all([s.callback.log == [] for s in diff_subs])
    # clear logs
    for s in subs + diff_subs:
        s.callback.log = []
    await asyncio.gather(*(p.publish(TOPIC, id(p)) for p in pubs))    
    pub_ids = {id(p) for p in pubs} 
    assert all([set(s.callback.log) == pub_ids for s in subs])
    assert all([set(s.callback.log) == set() for s in diff_subs])
