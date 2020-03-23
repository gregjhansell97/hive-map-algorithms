#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

from benchmarks.helpers import monitor
import pytest


class A:
    def run(self):
        return 1

def test_monitor():
    a = A()
    a = monitor(a, {"run": []})
    assert a.run() == 1
