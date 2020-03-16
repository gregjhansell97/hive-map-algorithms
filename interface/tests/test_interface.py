#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for interface
"""

import asyncio
import math
import pytest

from interface import Publisher, Subscriber, Router, Transceiver


def test_abstraction():
    """
    Create subclasses that do not implement methods, value errors expected
    """

    class T(Transceiver):
        pass

    class P(Publisher):
        pass

    class S(Subscriber):
        pass

    class R(Router):
        pass

    sub_classes = [T, P, S, R]
    for SubC in sub_classes:
        with pytest.raises(TypeError):
            c = SubC()


# creating classes with bare-minimum implementation
class T(Transceiver):
    def transmit(self, data):
        raise NotImplementedError


class P(Publisher):
    def publish(self, data):
        raise NotImplementedError


class S(Subscriber):
    async def on_recv(self, trx, data):
        raise NotImplementedError


class R(Router):
    async def on_recv(self, trx, data):
        raise NotImplementedError


ID = 0
TOPIC = 1


def test_transceiver_max_msg_size():
    t = T()
    assert t.max_msg_size == math.inf


def test_transceiver_subscription():
    async def cb(trx, data):
        cb.log.append((trx, data))

    cb.log = []
    t = T()
    t.subscribe(cb)
    asyncio.run(t.receive("some data"))
    assert cb.log == [(t, "some data")]


def test_publisher_use():
    t = T()
    p = P(ID, TOPIC)
    p.use(t)


def test_subscriber_use():
    t = T()
    s = S(ID, TOPIC)
    s.use(t)


def test_router_use():
    t = T()
    r = R(ID)
    r.use(t)
