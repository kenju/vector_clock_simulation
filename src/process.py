#!/usr/bin/env python3

from typing import List

from .event import Event


class Process:
    def __init__(self, process_id: int, events: List[Event]):
        self.id = process_id
        self.events = events
        self.timestamp = 0

    def __str__(self):
        events_str = ', '.join([str(e) for e in self.events])
        return f'P{self.id} [{events_str}]'
