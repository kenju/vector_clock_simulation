#!/usr/bin/env python3

import unittest

from .event import EventMessageRecv, EventInstruction, EventMessageSend
from .lamport_timestamps import LamportTimestampSolver
from .logger import Logger, LogLevel
from .message import Message
from .process import Process


class LamportTimestampTest(unittest.TestCase):
    def test_process_exampleA(self):
        # initialize messages
        m1 = Message(1)
        m2 = Message(2)
        m3 = Message(3)
        m4 = Message(4)
        m5 = Message(5)
        m6 = Message(6)
        m7 = Message(7)
        m8 = Message(8)
        m9 = Message(9)
        m10 = Message(10)

        # initialize events
        p0 = Process(
            process_id=0,
            events=[
                EventMessageSend(m1),
                EventMessageRecv(m3),
                EventMessageRecv(m5),
                EventInstruction(),
                EventMessageSend(m8),
            ],
        )
        p1 = Process(
            process_id=1,
            events=[
                EventInstruction(),
                EventMessageSend(m3),
                EventMessageRecv(m2),
                EventMessageSend(m4),
                EventMessageSend(m5),
                EventInstruction(),
                EventMessageSend(m7),
                EventMessageRecv(m10),
            ],
        )
        p2 = Process(
            process_id=2,
            events=[
                EventMessageRecv(m1),
                EventMessageSend(m2),
                EventMessageSend(m6),
                EventInstruction(),
                EventMessageRecv(m8),
                EventMessageSend(m9),
                EventMessageRecv(m4),
            ],
        )
        p3 = Process(
            process_id=3,
            events=[
                EventInstruction(),
                EventMessageRecv(m7),
                EventMessageRecv(m6),
                EventMessageRecv(m9),
                EventMessageSend(m10),
            ],
        )

        logger = Logger(LogLevel.DEBUG)
        logger.set_logfile("log/test_lamport_exampleA.log")
        processes = [p0, p1, p2, p3]
        lamport = LamportTimestampSolver(logger, processes)

        lamport.print()

        self.assertEqual(lamport.total_event_count(), 25)

        processed = lamport.process()
        self.assertListEqual(processed[p0], [1, 3, 7, 8, 9])
        self.assertListEqual(processed[p1], [1, 2, 4, 5, 6, 7, 8, 14])
        self.assertListEqual(processed[p2], [2, 3, 4, 5, 10, 11, 12])
        self.assertListEqual(processed[p3], [1, 9, 10, 12, 13])

    def test_process_exampleB(self):
        # initialize messages
        m1 = Message(1)
        m2 = Message(2)
        m3 = Message(3)
        m4 = Message(4)
        m5 = Message(5)
        m6 = Message(6)
        m7 = Message(7)
        m8 = Message(8)
        m9 = Message(9)
        m10 = Message(10)

        # initialize events
        p0 = Process(
            process_id=0,
            events=[
                EventMessageSend(m1),
                EventInstruction(),
                EventMessageRecv(m7),
                EventMessageSend(m8),
                EventInstruction(),
                EventInstruction(),
                EventMessageRecv(m10),
            ],
        )
        p1 = Process(
            process_id=1,
            events=[
                EventMessageRecv(m3),
                EventMessageSend(m6),
                EventMessageSend(m7),
            ],
        )
        p2 = Process(
            process_id=2,
            events=[
                EventMessageRecv(m2),
                EventMessageSend(m4),
                EventMessageSend(m3),
                EventMessageRecv(m1),
                EventMessageSend(m5),
                EventInstruction(),
                EventMessageRecv(m8),
                EventMessageSend(m9),
                EventMessageRecv(m6),
            ],
        )
        p3 = Process(
            process_id=3,
            events=[
                EventMessageSend(m2),
                EventMessageRecv(m4),
                EventMessageRecv(m5),
                EventInstruction(),
                EventMessageRecv(m9),
                EventMessageSend(m10),
            ],
        )

        logger = Logger(LogLevel.DEBUG)
        logger.set_logfile("log/test_lamport_exampleB.log")
        processes = [p0, p1, p2, p3]
        lamport = LamportTimestampSolver(logger, processes)

        lamport.print()

        self.assertEqual(lamport.total_event_count(), 25)

        processed = lamport.process()
        self.assertListEqual(processed[p0], [1, 2, 8, 9, 10, 11, 14])
        self.assertListEqual(processed[p1], [5, 6, 7])
        self.assertListEqual(processed[p2], [2, 3, 4, 5, 6, 7, 10, 11, 12])
        self.assertListEqual(processed[p3], [1, 4, 7, 8, 12, 13])

    def test_process_exampleC(self):
        # initialize messages
        m1 = Message(1)
        m2 = Message(2)
        m3 = Message(3)
        m4 = Message(4)
        m5 = Message(5)
        m6 = Message(6)
        m7 = Message(7)
        m8 = Message(8)
        m9 = Message(9)
        m10 = Message(10)
        m11 = Message(11)

        # initialize events
        p1 = Process(
            process_id=1,
            events=[
                EventMessageSend(m1),
                EventMessageSend(m2),
                EventMessageSend(m3),
                EventMessageRecv(m7),
                EventMessageSend(m4),
                EventMessageSend(m5),
            ],
        )
        p2 = Process(
            process_id=2,
            events=[
                EventMessageRecv(m8),
                EventMessageSend(m6),
                EventMessageSend(m7),
                EventMessageRecv(m10),
                EventMessageRecv(m2),
            ],
        )
        p3 = Process(
            process_id=3,
            events=[
                EventMessageRecv(m9),
                EventMessageSend(m8),
                EventMessageRecv(m1),
                EventMessageRecv(m4),
                EventMessageRecv(m6),
                EventMessageRecv(m11),
                EventMessageRecv(m5),
            ],
        )
        p4 = Process(
            process_id=4,
            events=[
                EventMessageSend(m9),
                EventMessageSend(m10),
                EventMessageRecv(m3),
                EventMessageSend(m11),
            ],
        )

        logger = Logger(LogLevel.DEBUG)
        logger.set_logfile("log/test_lamport_exampleC.log")
        processes = [p1, p2, p3, p4]
        lamport = LamportTimestampSolver(logger, processes)

        lamport.print()

        self.assertEqual(lamport.total_event_count(), 22)

        processed = lamport.process()
        self.assertListEqual(processed[p1], [1, 2, 3, 7, 8, 9])
        self.assertListEqual(processed[p2], [4, 5, 6, 7, 8])
        self.assertListEqual(processed[p3], [2, 3, 4, 9, 10, 11, 12])
        self.assertListEqual(processed[p4], [1, 2, 4, 5])


if __name__ == '__main__':
    unittest.main()
