#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from helpers import connect, get_uid
from algorithms import flood
import time

TOPIC = 1
async def periodic_publish(p, rate, bias=0.0, duration=10):
    start_time = time.time()
    await asyncio.sleep(bias)
    while time.time() - start_time < duration:
        # publisher here!
        t = time.time() - start_time
        await asyncio.gather(p.publish(TOPIC, f"{p}:{t}"), asyncio.sleep(rate))

async def callback(data):
    pass
async def main(Publisher, Subscriber, Router):
    rtrs = [Router(uid=f"R{i}") for i in range(4)]
    subs = [
            Subscriber(callback=callback, topic=TOPIC, uid=f"S{i}") 
            for i in range(5)]
    pubs = [Publisher(uid=f"P{i}") for i in range(2)]

    connect([pubs[0], subs[0], rtrs[0]])
    connect([rtrs[0], rtrs[1]])
    connect([rtrs[1], rtrs[2], subs[1]])
    connect([rtrs[2], pubs[1]])
    connect([pubs[1], subs[2]])
    connect([subs[3], rtrs[3], subs[4]])

    coros = (
            periodic_publish(pubs[0], 0.5),
            periodic_publish(pubs[1], 0.5, bias=0.25)
    )
    await asyncio.gather(*coros)
    # TODO evaluate statistics
    # TODO consider using numbers exclusivly (to write optimize evaluation)
    # successful accepts
    sub_logs = [
            set(s.logs[1])
            for s in subs]
    ideal_delivery = 0
    delivery = 0
    for p in pubs:
        t, messages = p.logs
        for action, topic, data in messages:
            # should get to every subscriber
            for messages in sub_logs:
                if ("accepted", topic, data) in messages:
                    delivery +=1 
            ideal_delivery += len(sub_logs)
    print(f"Successful message ratio: {delivery/ideal_delivery}")
    # total messages rejected
    for c in subs + rtrs:
        total += 



if __name__ == "__main__":
    asyncio.run(main(flood.Publisher, flood.Subscriber, flood.Router))
