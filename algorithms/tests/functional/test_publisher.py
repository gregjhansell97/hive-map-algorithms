#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests for Publisher
"""

from collections import defaultdict
import pytest

from pub_sub_interface.trxs import LocalTransceiver

def test_initialization(algorithm):
    """
    Verify publisher can take in a topic and not crash
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(10)


def test_use_local_transceiver(algorithm):
    """
    Verify publisher can use a transceiver object
    """
    Publisher, Subscriber, Router = algorithm
    # set up publisher
    p = Publisher(10)
    t = LocalTransceiver()
    p.use(t)


def test_use_multiple_local_transceivers(algorithm):
    """
    Verify publisher can use multiple transceivers
    """
    Publisher, Subscriber, Router = algorithm
    # set up publisher
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)


def test_publish_no_transceiver(algorithm):
    """
    Verify publisher can publish even with no means of transceiver. May want to
    consider raising an error if publish is called with no tranceiver...
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    p.publish(b"hello world")


def test_publish_one_local_transceiver(algorithm):
    """
    Verify publish works with when using one tranceiver
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    t = LocalTransceiver()
    p.use(t)
    p.publish(b"hello world")


def test_publish_many_transceivers(algorithm):
    """
    Verify publish works with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    p.publish(b"goodbye yellow brick road")


def test_many_publish_many_transceivers(algorithm):
    """
    Verify publish works many times with when using multiple tranceivers
    """
    Publisher, Subscriber, Router = algorithm
    p = Publisher(5)
    ts = [LocalTransceiver() for _ in range(10)]
    for t in ts:
        p.use(t)
    for i in range(10):
        p.publish(b"goodbye yellow brick road")
