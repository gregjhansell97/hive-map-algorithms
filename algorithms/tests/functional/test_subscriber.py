#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Subscriber. Does not test actual receiving of messages, that is
in the system tests
"""

import pytest

from transceivers import LocalTransceiver
from tests.functional.helpers import get_callback

def test_initialization(algorithm):
    """
    Verifies subscriber can take in a topic and callback without crashing
    """
    Publisher, Subscriber, Router = algorithm
    cb = get_callback()
    s = Subscriber(uid="id", topic=10, callback=cb)


def test_use_local_transceiver(algorithm):
    """
    Verifies subscriber can use a transceiver without crashing
    """
    Publisher, Subscriber, Router = algorithm
    cb = get_callback()
    # set up publisher
    s = Subscriber(uid="id", topic=10, callback=cb)
    t = LocalTransceiver()
    s.use(t)


def test_use_multiple_Local_transceivers(algorithm):
    """
    Verifies subscriber can use multiple tranceivers without crashing
    """
    Publisher, Subscriber, Router = algorithm
    # set up publisher
    cb = get_callback()
    s = Subscriber(uid="id", topic=5, callback=cb)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        s.use(t)
