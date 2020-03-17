#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""
def get_callback():
    """
    Creates a callback instance that tracks invocations. This function was
    created because a lot of tests create a callback, especially the system
    tests!
    
    Returns (lambda d): callback that takes in data as argument
    """

    async def cb(data):
        # callbacks for transceivers expects a transceiver instance and
        # raw-bytes being received
        cb.log.append(data)

    cb.log = []  # log tracks the data received and by which transceiver
    return cb
