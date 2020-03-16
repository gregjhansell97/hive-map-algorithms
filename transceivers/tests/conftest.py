#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Dummy conftest.py for transceiver

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    https://pytest.org/latest/plugins.html
"""

from transceivers import LocalTransceiver, EuclideanTransceiver

def pytest_generate_tests(metafunc):
    """
    Customize test functions however needed
    """
    if "LT" in metafunc.fixturenames:
        # parameterzed local transceivers
        transceiver_classes = [
                LocalTransceiver,
                EuclideanTransceiver
        ]
        metafunc.parametrize("LT", transceiver_classes)
    if "ET" in metafunc.fixturenames:
        # parameterzed local transceivers
        transceiver_classes = [
                EuclideanTransceiver
        ]
        metafunc.parametrize("ET", transceiver_classes)
