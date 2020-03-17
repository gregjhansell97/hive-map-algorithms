#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for pub_sub_interface.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from algorithms import flood

def pytest_generate_tests(metafunc):
    """
    Customize test functions however needed
    """
    if "algorithm" in metafunc.fixturenames:
        # parameterized algorithms
        algorithms = [
                (flood.Publisher, flood.Subscriber, flood.Router)
        ]
        metafunc.parametrize("algorithm", algorithms)
