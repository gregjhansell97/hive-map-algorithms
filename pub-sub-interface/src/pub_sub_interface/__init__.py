# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

from pub_sub_interface.publisher import Publisher
from pub_sub_interface.subscriber import Subscriber
from pub_sub_interface.router import Router
from pub_sub_interface.transceiver import Transceiver

__all__ = ["Publisher", "Subscriber", "Router"]

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = 'pub-sub-interface'
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
