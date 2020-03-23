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
    async def on_recv(self, trx, data, context):
        raise NotImplementedError


class R(Router):
    async def on_recv(self, trx, data, context):
        raise NotImplementedError


def get_trx_callback():
    async def cb(trx, data):
        cb.log += [(trx, data)]

    cb.log = []
    return cb


ID = "ID"
TOPIC = 1


def CALLBACK(data):
    pass


def test_transceiver():
    t = T()
    assert str(t) == f"{id(t)}"
    assert t.transmit_strength == 1
    assert t.receive_strength == 1
    time = t.time
    assert t.max_msg_size == math.inf


@pytest.mark.asyncio
async def test_transceiver_subscription():
    t = T()
    for i in range(10):
        t.subscribe(get_trx_callback())
    await t.receive("d")
    await t.receive("m")
    assert all([cb.log == [(t, "d"), (t, "m")] for cb in t.callbacks])
    await t.log("test complete")
    t.logs == ["test complete"]


def test_missing_args():
    """
    Create subclasses that do not implement methods, value errors expected
    """
    sub_classes = [P, S, R]
    for SubC in sub_classes:
        with pytest.raises(TypeError):
            c = SubC()


def test_publisher():
    t = T()
    p = P(uid=ID)
    p.use(t)
    assert str(p) == ID


def test_subscriber():
    t = T()
    s = S(uid=ID, topic=TOPIC, callback=CALLBACK)
    s.use(t)
    assert str(s) == ID


def test_router():
    t = T()
    r = R(uid=ID)
    r.use(t)
    assert str(r) == ID
