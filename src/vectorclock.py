#!/usr/bin/env python3

from typing import List

from .logger import Logger
from .process import Process
from .solver import Solver
from .timestamp import Timestamp


class VectorClockTimestamp(Timestamp):
    def __init__(self, length: int) -> None:
        super().__init__()
        self._timestamp = [0 for _ in range(length)]

    def incr(self, process_id):
        self._timestamp[process_id] += 1

    def get(self) -> List[int]:
        return self._timestamp

    def merge(self, process_id: int, other: 'VectorClockTimestamp'):
        merged = []
        local_ts = self.get()
        other_ts = other.get()
        for idx, t in enumerate(local_ts):
            if idx == process_id:
                m = max(t, other_ts[idx]) + 1
            else:
                m = max(t, other_ts[idx])
            merged.append(m)
        self._timestamp = merged


class VectorClockTimestampSolver(Solver):
    def __init__(
        self,
        logger: Logger,
        processes: List[Process],
    ):
        super().__init__(
            logger=logger,
            processes=processes,
            timestamp_class=VectorClockTimestamp,
            timestamp_class_args={
                'length': len(processes),
            },
        )
