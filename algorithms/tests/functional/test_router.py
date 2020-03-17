#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Router. Does not test actual receiving of messages, that is
in the system tests
"""

from collections import defaultdict
import pytest

from transceivers import LocalTransceiver


def test_initialization(algorithm):
    """
    Verifies router can take in a topic and callback without crashing
    """
    Publisher, Subscriber, Router = algorithm
    r = Router()


def test_use_transceiver(algorithm):
    """
    Verifies subscriber can use a transceiver without crashing
    """
    Publisher, Subscriber, Router = algorithm
    r = Router()
    t = LocalTransceiver()
    r.use(t)


def test_use_multiple_transceivers(algorithm):
    """
    Verifies subscriber can use multiple tranceivers without crashing
    """
    Publisher, Subscriber, Router = algorithm
    r = Router()
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        r.use(t)
