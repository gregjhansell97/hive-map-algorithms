#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Subscriber. Does not test actual receiving of messages, that is
in the system tests
"""

from collections import defaultdict
import pytest

from tests.transceivers import LocalTransceiver

def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback, especially the system
    tests!
    
    Returns (lambda d): callback that takes in data as argument
    """

    def cb(data):
        # callbacks for transceivers expects a transceiver instance and
        # raw-bytes being received
        cb.log.append(data)

    cb.log = []  # log tracks the data received and by which transceiver
    return cb


def test_initialization(algorithm):
    """
    Verifies subscriber can take in a topic and callback without crashing
    """
    Publisher, Subscriber, Router = algorithm
    cb = get_callback()
    s = Subscriber(10, cb)


def test_use_local_transceiver(algorithm):
    """
    Verifies subscriber can use a transceiver without crashing
    """
    Publisher, Subscriber, Router = algorithm
    cb = get_callback()
    # set up publisher
    s = Subscriber(10, cb)
    t = LocalTransceiver()
    s.use(t)


def test_use_multiple_Local_transceivers(algorithm):
    """
    Verifies subscriber can use multiple tranceivers without crashing
    """
    Publisher, Subscriber, Router = algorithm
    # set up publisher
    cb = get_callback()
    s = Subscriber(5, cb)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        s.use(t)
