#!/usr/bin/env python3

from enum import Enum

class MessageState(Enum):
    NOT_READY = 1
    SENDING = 2
    RECEIVED = 3


class Message:
    def __init__(self, message_id: int):
        self.id = message_id
        self.state = MessageState.NOT_READY
        self._value = None

    def __str__(self):
        return f'M{self.id}'

    def get(self):
        return self._value

    def send(self, value):
        self.state = MessageState.SENDING
        self._value = value

    def receive(self):
        self.state = MessageState.RECEIVED
        return self._value
