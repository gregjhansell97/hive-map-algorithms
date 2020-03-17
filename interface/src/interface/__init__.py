# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

from interface.publisher import Publisher
from interface.subscriber import Subscriber
from interface.router import Router
from interface.transceiver import Transceiver

__all__ = ["Publisher", "Subscriber", "Router", "Transceiver"]

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = "interface"
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
