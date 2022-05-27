from typing import List, Dict, Optional

from .process import Process
from .timestamp import Timestamp


class State:
    def __init__(
        self,
        process_id: int,
        timestamp_class: Timestamp,
        timestamp_class_args: Optional[Dict],
    ) -> None:
        self._process_id = process_id
        self._timestamp = timestamp_class(**timestamp_class_args)
        self._current_event_idx = 0

    def incr_timestamp(self):
        self._timestamp.incr(self._process_id)

    def get_timestamp(self) -> Timestamp:
        return self._timestamp

    def merge(self, timestamp: Timestamp):
        self._timestamp.merge(self._process_id, timestamp)

    def incr_event_idx(self):
        self._current_event_idx += 1

    def current_event_idx(self) -> int:
        return self._current_event_idx


class States:
    def __init__(
        self,
        processes: List[Process],
        timestamp_class: Timestamp,
        timestamp_class_args: Optional[Dict],
    ) -> None:
        states: Dict[Process, State] = {}
        for process in processes:
            states[process] = State(
                process_id=process.id,
                timestamp_class=timestamp_class,
                timestamp_class_args=timestamp_class_args,
            )
        self._states = states
        self.current_id = 0

    def incr_timestamp(self, process: Process):
        self._states[process].incr_timestamp()

    def get_timestamp(self, process: Process) -> Timestamp:
        return self._states[process].get_timestamp()

    def merge(self, process: Process, sent_timestamp: Timestamp):
        self._states[process].merge(sent_timestamp)

    def incr_event_idx(self, process: Process):
        self._states[process].incr_event_idx()

    def current_event_idx(self, process: Process) -> int:
        return self._states[process].current_event_idx()
