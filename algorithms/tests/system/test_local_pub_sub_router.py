#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests pub-sub network with routers involved
"""

import asyncio
import pytest

from tests.functional.helpers import get_callback
from tests.system.helpers import TOPIC, DIFF_TOPIC, connect

@pytest.mark.asyncio
async def test_one_pub_one_sub_one_router_over_local_connection(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them both
    to a router
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(uid="P")
    s = Subscriber(uid="S", topic=TOPIC, callback=get_callback())
    r = Router(uid="R")
    # connections
    connect([p, r]) # publisher and router connection
    connect([s, r]) # subscriber and router connection
    # verification
    await asyncio.gather(*(p.publish(TOPIC, i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))

@pytest.mark.asyncio
async def test_one_pub_one_sub_router_love_triangle_over_local_connections(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them to
    different routers and then connect all routers together
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(uid="P")
    s = Subscriber(uid="S", topic=TOPIC, callback=get_callback())
    routers = [Router(uid="R") for i in range(3)]
    # connections
    connect([p, routers[0]]) # publisher and router connection
    connect([s, routers[1]]) # subscriber and router connection
    connect(routers)
    await asyncio.gather(*(p.publish(TOPIC, i) for i in range(10)))
    assert set(s.callback.log) == set(range(10))

#TODO confirm multiple connections on a router

