#!/usr/bin/env python3

from typing import List, Dict, Optional
from copy import deepcopy

from .event import EventType
from .logger import Logger
from .message import Message, MessageState
from .process import Process
from .timestamp import Timestamp
from .states import States

class Solver():
    def __init__(
        self,
        logger: Logger,
        processes: List[Process],
        timestamp_class: Timestamp,
        timestamp_class_args: Optional[Dict],
    ):
        self.processes = processes
        self._logger = logger
        self._timestamp_class = timestamp_class
        self._timestamp_class_args = timestamp_class_args
        self._processed_cache = None

    def __str__(self) -> str:
        processes_str = '\n'.join([str(p) for p in self.processes])
        return f'{processes_str}'

    def print(self) -> None:
        self._logger.debug(self)

    def total_event_count(self) -> int:
        num_total_events = 0
        for process in self.processes:
            for _ in process.events:
                num_total_events += 1
        return num_total_events

    def concurrent_events(self, another: List[int]) -> List[int]:
        concurrent_events = []
        processed = self.process()
        for _, events in processed.items():
            for event in events:
                if event == another:
                    # same event
                    continue
                if all(x >= another[i] for i, x in enumerate(event)):
                    # E1 happens after E2
                    continue
                if all(x <= another[i] for i, x in enumerate(event)):
                    # E1 happens before E2
                    continue
                concurrent_events.append(event)
        return concurrent_events

    def process(self) -> Dict[Process, List[int]]:
        if self._processed_cache is not None:
            self._logger.debug('Solver#process() return from the local memory cache')
            return self._processed_cache

        # key = process
        # value = list of timestamp per events
        result = {}
        for process in self.processes:
            result[process] = []

        states = States(
            processes=self.processes,
            timestamp_class=self._timestamp_class,
            timestamp_class_args=self._timestamp_class_args,
        )

        while True:
            current_process = self.processes[states.current_id]
            for i, event in enumerate(current_process.events):

                pt = states.current_event_idx(current_process)
                if i < pt:
                    # already checked, skipping
                    continue

                ts = states.get_timestamp(current_process).get()
                self._logger.debug(
                    f'Handling P{current_process.id} {event} t={ts}...')

                # check if possible to proceed
                if event.event_type == EventType.INST:
                    self._logger.debug('instruction executed')
                    states.incr_timestamp(current_process)
                    local_timestamp = states.get_timestamp(current_process)
                    # deepcopy is required when timestamp is List/Dict/Clas, etc. ...
                    copied = deepcopy(local_timestamp.get())
                    result[current_process].append(copied)
                else:
                    # if not instruction, the event should be EventMessage
                    message: Message = event.message

                    if message.state == MessageState.NOT_READY:
                        if event.event_type == EventType.SEND:
                            states.incr_timestamp(current_process)
                            local_timestamp = states.get_timestamp(current_process)
                            # deepcopy is required when timestamp is List/Dict/Clas, etc. ...
                            copied = deepcopy(local_timestamp)
                            message.send(copied)
                            self._logger.debug(
                                f'{message} sent with value={copied.get()}')
                            result[current_process].append(copied.get())
                        else:
                            self._logger.debug(
                                f'{message} is not sent, should wait')
                            break
                    elif message.state == MessageState.SENDING:
                        if event.event_type == EventType.RECV:
                            sent_timestamp = message.receive()
                            self._logger.debug(
                                f'{message} received with value={sent_timestamp.get()}')
                            states.merge(current_process, sent_timestamp)
                            merged = states.get_timestamp(current_process)
                            self._logger.debug(f'merged value is {merged.get()}')
                            # deepcopy is required when timestamp is List/Dict/Clas, etc. ...
                            copied = deepcopy(merged.get())
                            result[current_process].append(copied)
                        else:
                            # if it's in sending state, it should be skipped
                            self._logger.debug(
                                f'{message} is still sending, should wait')
                            break
                    elif message.state == MessageState.RECEIVED:
                        raise Exception(
                            """this cannot be called, since it always goes to
                            next event after receiving message""")
                    else:
                        raise ValueError(f'unsupported type {event.event_type}')

                states.incr_event_idx(current_process)

            # no more events to check in the current process, go to next
            if states.current_id == len(self.processes) - 1:
                states.current_id = 0
            else:
                states.current_id += 1

            # no more events to check for all processes, finish
            finished = True
            for process in self.processes:
                if states.current_event_idx(process) != len(process.events):
                    finished = False
            if finished:
                break

        self._processed_cache = result
        return result
