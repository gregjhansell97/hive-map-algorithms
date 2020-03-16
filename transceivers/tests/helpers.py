#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides helpful functions for tests
"""
import pytest


def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """

    async def cb(trx, data):
        # callbacks for transceivers expects a transceiver instance, a time,
        # and data
        cb.log.append((trx, data))

    cb.log = []  # log tracks the data received and by which transceiver
    return cb
