#!/usr/bin/
# -*- coding: utf-8 -*-

#from transceivers import BenchmarkTransceiver as Transceiver

def run():
    """
    I want this to take in a YAML or JSON file.
    Parameters:
    1. List of Algorithms by name to benchmark
    3. Map size
    4. Simulation duration
    2. List of nodes describing:
        - location
        - type(publisher, subscriber, router)
            - specific attributes for type
        - velocity
        - communication range
        - likelyhood of successful receive
        - broadcast delays
        - time of arrival
        - time of done
    3. File name to dump raw data to
    4. TODO: create something that takes in raw data and creates plots out of it
        this will be really important when we run it on the supercomputer:
        - heatmaps
        - gifs
        - graphs
    """
    print("hello world")
