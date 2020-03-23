#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides helpful functions for tests
"""
import pytest

from interface import Transceiver

def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """
    async def cb(trx, data):
        cb.log.append((trx, data))
    cb.log = []
    return cb
