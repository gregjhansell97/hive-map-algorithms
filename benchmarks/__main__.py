#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Entry point for benchmarks
"""

from multiprocessing import Process, Queue
import uuid

def spawn_master_node(incoming_q, outgoing_qs):
    while True:
        msg = incoming_q.get()
        if msg == None:
            break
        for q in outgoing_qs:
            q.put(msg)

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
    transmit_q = Queue()
    receive_qs = [Queue() for _ in range(3)]

    master = Process(target=spawn_master_node, args=(transmit_q, receive_qs))

    spawn_master_node()
    # based on file input spawn routers, subscribers and publishers
    # NOTE: routers, subscribers and publishers are all separate processes

    # sleep for duration of simulation
    # "poison pill" all nodes which stops them once queue is empty
    # NOTE: poison pill should prevent publishers from publishing anything 
    # new and waits for system to reach steady state before stoping so that
    # all nodes are in the clear





    pass
