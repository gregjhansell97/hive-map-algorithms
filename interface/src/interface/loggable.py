#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC
from time import process_time


class Loggable(ABC):
    def __init__(self):
        self._time = []
        self._action = []
        self._topic = []
        self._data = []

    @property
    def logs(self):
        return (self._time, self._action, self._topic, self._data)

    async def log(self, info):
        # may want to consider puting in separate thread and locking it up
        self._time.append(process_time())
        self._action.append(action)
        self._topic.append(topic)
        self._data.append(data)
