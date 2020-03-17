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

class Callback(Transceiver.Callback):
    def __init__(self): 
        super().__init__()
        self.log = []
    async def relevant(self, context):
        return context != "irrelevant" and await super().relevant(context)
    async def on_recv(self, trx, data, context):
        self.log.append((trx, data, context))


class P(Publisher):
    def publish(self, data):
        raise NotImplementedError


class S(Subscriber):
    async def on_recv(self, trx, data, context):
        raise NotImplementedError


class R(Router):
    async def on_recv(self, trx, data, context):
        raise NotImplementedError


ID = 0
TOPIC = 1
CALLBACK = None


def test_transceiver_max_msg_size():
    t = T()
    assert t.max_msg_size == math.inf


@pytest.mark.asyncio
async def test_transceiver_subscription():
    t = T()
    t.subscribe(Callback())
    await t.receive("data", "context")
    await t.receive("ignore", "irrelevant")
    assert all([cb.log == [(t, "data", "context")] for cb in t.callbacks])


def test_publisher_use():
    t = T()
    p = P(ID, TOPIC)
    p.use(t)


def test_subscriber_use():
    t = T()
    s = S(ID, TOPIC, CALLBACK)
    s.use(t)


def test_router_use():
    t = T()
    r = R(ID)
    r.use(t)
