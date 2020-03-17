#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests pub-sub network without routers involved, mostly analyzes the interaction
between subscribers and publishers
"""

from transceivers import LocalTransceiver

__all__ = ["TOPIC", "DIFF_TOPIC", "connect"]

TOPIC = 10
DIFF_TOPIC = 11
def connect(components):
    trxs = [LocalTransceiver() for _ in components]
    LocalTransceiver.connect(trxs)
    for c, t in zip(components, trxs):
        c.use(t)
