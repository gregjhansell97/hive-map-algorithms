#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests pub-sub network with routers involved
"""

import pytest

from tests.functional.test_subscriber import get_callback
from pub_sub_interface.trxs import LocalTransceiver


def test_one_pub_one_sub_one_router_over_local_connection(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them both
    to a router
    """
    Publisher, Subscriber, Router = algorithm
    TOPIC = 10
    p = Publisher(TOPIC)
    cb = get_callback()
    s = Subscriber(TOPIC, cb)
    r = Router()
    LocalTransceiver.connect([p, r]) # publisher and router connection
    LocalTransceiver.connect([s, r]) # subscriber and router connection
    p.publish("hello")
    assert cb.log == ["hello"]
    p.publish("goodbye")
    assert cb.log == ["hello", "goodbye"]

def test_one_pub_one_sub_router_love_triangle_over_local_connections(algorithm):
    """
    Get one publisher instance and one subscriber instance and connect them to
    different routers and then connect all routers together
    """
    Publisher, Subscriber, Router = algorithm
    TOPIC = 10
    p = Publisher(TOPIC)
    cb = get_callback()
    s = Subscriber(TOPIC, cb)
    routers = [Router() for i in range(3)]
    LocalTransceiver.connect([p, routers[0]]) # publisher and router connection
    LocalTransceiver.connect([s, routers[1]]) # subscriber and router connection
    LocalTransceiver.connect(routers)
    p.publish("hello")
    assert cb.log == ["hello"]


