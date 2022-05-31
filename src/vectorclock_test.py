import unittest

from .event import EventMessageRecv, EventInstruction, EventMessageSend
from .logger import Logger, LogLevel
from .message import Message
from .vectorclock import VectorClockTimestampSolver
from .process import Process


class VectorClockTimestampTest(unittest.TestCase):
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
        logger.set_logfile("log/test_vectorclock_exampleA.log")

        processes = [p0, p1, p2, p3]
        vectorclock = VectorClockTimestampSolver(logger, processes)
        vectorclock.print()

        self.assertEqual(vectorclock.total_event_count(), 25)

        processed = vectorclock.process()
        self.assertListEqual(processed[p0], [
            [1, 0, 0, 0],
            [2, 2, 0, 0],
            [3, 5, 2, 0],
            [4, 5, 2, 0],
            [5, 5, 2, 0],
        ])
        self.assertListEqual(processed[p1], [
            [0, 1, 0, 0],
            [0, 2, 0, 0],
            [1, 3, 2, 0],
            [1, 4, 2, 0],
            [1, 5, 2, 0],
            [1, 6, 2, 0],
            [1, 7, 2, 0],
            [5, 8, 6, 5],
        ])
        self.assertListEqual(processed[p2], [
            [1, 0, 1, 0],
            [1, 0, 2, 0],
            [1, 0, 3, 0],
            [1, 0, 4, 0],
            [5, 5, 5, 0],
            [5, 5, 6, 0],
            [5, 5, 7, 0],
        ])
        self.assertListEqual(processed[p3], [
            [0, 0, 0, 1],
            [1, 7, 2, 2],
            [1, 7, 3, 3],
            [5, 7, 6, 4],
            [5, 7, 6, 5],
        ])

        concurrent_events = vectorclock.concurrent_events(
            another=[1, 4, 2, 0],
        )
        self.assertListEqual(concurrent_events, [
            [2, 2, 0, 0],
            [1, 0, 3, 0],
            [1, 0, 4, 0],
            [0, 0, 0, 1],
        ])

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
        logger.set_logfile("log/test_vectorclock_exampleB.log")

        processes = [p0, p1, p2, p3]
        vectorclock = VectorClockTimestampSolver(logger, processes)
        vectorclock.print()

        self.assertEqual(vectorclock.total_event_count(), 25)

        processed = vectorclock.process()
        self.assertListEqual(processed[p0], [
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [3, 3, 3, 1],
            [4, 3, 3, 1],
            [5, 3, 3, 1],
            [6, 3, 3, 1],
            [7, 3, 8, 6],
        ])
        self.assertListEqual(processed[p1], [
            [0, 1, 3, 1],
            [0, 2, 3, 1],
            [0, 3, 3, 1],
        ])
        self.assertListEqual(processed[p2], [
            [0, 0, 1, 1],
            [0, 0, 2, 1],
            [0, 0, 3, 1],
            [1, 0, 4, 1],
            [1, 0, 5, 1],
            [1, 0, 6, 1],
            [4, 3, 7, 1],
            [4, 3, 8, 1],
            [4, 3, 9, 1],
        ])
        self.assertListEqual(processed[p3], [
            [0, 0, 0, 1],
            [0, 0, 2, 2],
            [1, 0, 5, 3],
            [1, 0, 5, 4],
            [4, 3, 8, 5],
            [4, 3, 8, 6],
        ])

        concurrent_events = vectorclock.concurrent_events(
            another=[0, 2, 3, 1],
        )
        self.assertListEqual(concurrent_events, [
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [1, 0, 4, 1],
            [1, 0, 5, 1],
            [1, 0, 6, 1],
            [0, 0, 2, 2],
            [1, 0, 5, 3],
            [1, 0, 5, 4],
        ])


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
        p0 = Process(
            process_id=0,
            events=[
                EventMessageSend(m1),
                EventMessageSend(m2),
                EventMessageSend(m3),
                EventMessageRecv(m7),
                EventMessageSend(m4),
                EventMessageSend(m5),
            ],
        )
        p1 = Process(
            process_id=1,
            events=[
                EventMessageRecv(m8),
                EventMessageSend(m6),
                EventMessageSend(m7),
                EventMessageRecv(m10),
                EventMessageRecv(m2),
            ],
        )
        p2 = Process(
            process_id=2,
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
        p3 = Process(
            process_id=3,
            events=[
                EventMessageSend(m9),
                EventMessageSend(m10),
                EventMessageRecv(m3),
                EventMessageSend(m11),
            ],
        )

        logger = Logger(LogLevel.DEBUG)
        logger.set_logfile("log/test_vectorclock_exampleC.log")
        processes = [p0, p1, p2, p3]
        vectorclock = VectorClockTimestampSolver(logger, processes)

        vectorclock.print()

        self.assertEqual(vectorclock.total_event_count(), 22)

        processed = vectorclock.process()
        self.assertListEqual(processed[p0], [
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [3, 0, 0, 0],
            [4, 3, 2, 1],
            [5, 3, 2, 1],
            [6, 3, 2, 1],
        ])
        self.assertListEqual(processed[p1], [
            [0, 1, 2, 1],
            [0, 2, 2, 1],
            [0, 3, 2, 1],
            [0, 4, 2, 2],
            [2, 5, 2, 2],
        ])
        self.assertListEqual(processed[p2], [
            [0, 0, 1, 1],
            [0, 0, 2, 1],
            [1, 0, 3, 1],
            [5, 3, 4, 1],
            [5, 3, 5, 1],
            [5, 3, 6, 4],
            [6, 3, 7, 4],
        ])
        self.assertListEqual(processed[p3], [
            [0, 0, 0, 1],
            [0, 0, 0, 2],
            [3, 0, 0, 3],
            [3, 0, 0, 4],
        ])

        concurrent_events = vectorclock.concurrent_events(
            another=[0, 0, 0, 2],
        )
        self.assertListEqual(concurrent_events, [
            [1, 0, 0, 0],
            [2, 0, 0, 0],
            [3, 0, 0, 0],
            [4, 3, 2, 1],
            [5, 3, 2, 1],
            [6, 3, 2, 1],
            [0, 1, 2, 1],
            [0, 2, 2, 1],
            [0, 3, 2, 1],
            [0, 0, 1, 1],
            [0, 0, 2, 1],
            [1, 0, 3, 1],
            [5, 3, 4, 1],
            [5, 3, 5, 1],
        ])


if __name__ == '__main__':
    unittest.main()
