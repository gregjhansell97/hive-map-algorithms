#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides helpful functions for tests
"""
import pytest

from interface import Transceiver

class Callback(Transceiver.Callback):
    def __init__(self):
        super().__init__()
        self.log = []
    async def on_recv(self, trx, data, context):
        self.log.append((trx, data))

def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback!
    
    Returns (lambda t, d): callback that takes in a transceiver and data as
        arguments
    """

    return Callback()
