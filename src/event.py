#!/usr/bin/env python3

from enum import Enum

from .message import Message


class EventType(Enum):
    INST = 1
    SEND = 2
    RECV = 3


class Event:
    def __init__(self, event_type: EventType) -> None:
        self.event_type = event_type

    def __str__(self):
        return f'({self.event_type.name})'


class EventInstruction(Event):
    def __init__(self):
        super().__init__(EventType.INST)


class EventMessageSend(Event):
    def __init__(self, message: Message):
        super().__init__(EventType.SEND)
        self.message = message

    def __str__(self):
        return f'({self.message}_{self.event_type.name})'


class EventMessageRecv(Event):
    def __init__(self, message: Message):
        super().__init__(EventType.RECV)
        self.message = message

    def __str__(self):
        return f'({self.message}_{self.event_type.name})'
