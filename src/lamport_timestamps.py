#!/usr/bin/env python3

from typing import List

from .logger import Logger
from .process import Process
from .solver import Solver
from .timestamp import Timestamp


class LamportTimestamp(Timestamp):
    def __init__(self) -> None:
        super().__init__()
        self._timestamp = 0

    def incr(self, process_id: int):
        self._timestamp += 1

    def get(self) -> int:
        return self._timestamp

    def merge(self, process_id: int, other: Timestamp):
        merged = max(self.get(), other.get()) + 1
        self._timestamp = merged


class LamportTimestampSolver(Solver):
    def __init__(self, logger: Logger, processes: List[Process]):
        super().__init__(
            logger=logger,
            processes=processes,
            timestamp_class=LamportTimestamp,
            timestamp_class_args={},
        )
