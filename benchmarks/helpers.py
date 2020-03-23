#!/usr/bin/env python
# -*- coding: utf-8 -*-

from transceivers import LocalTransceiver

def connect(components):
    trxs = [LocalTransceiver() for _ in components]
    LocalTransceiver.connect(trxs)
    for c, t in zip(components, trxs):
        c.use(t)

def get_uid():
    id_ = get_uid.next_uid
    get_uid.next_uid += 1
get_uid.next_uid = 0

