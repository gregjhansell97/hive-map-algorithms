#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entry point for benchmarks
"""

import uuid

def spawn_master_node():
    pass

def spawn_router():
    pass

def spawn_subscriber():
    pass

def spawn_publisher():
    pass

if __name__ == "__main__":
    # End goal: read file that starts up routers, subscribers and publishers
    # create queues for routers, subscribers and publishers
    # spawn master node that handles broadcast and receive aspect of queues
    
    # create queues

    spawn_master_node()
    # based on file input spawn routers, subscribers and publishers
    # NOTE: routers, subscribers and publishers are all separate processes

    # sleep for duration of simulation
    # "poison pill" all nodes which stops them once queue is empty
    # NOTE: poison pill should prevent publishers from publishing anything 
    # new and waits for system to reach steady state before stoping so that
    # all nodes are in the clear





    pass
