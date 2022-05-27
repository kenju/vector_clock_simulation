# Vector Clock Simulation

Vector clock and Lamport simulation, written in Python.

- https://en.wikipedia.org/wiki/Vector_clock
- https://en.wikipedia.org/wiki/Lamport_timestamp

## Example

### Vector Clock

For example, let's imagine that you want to simulate the following case.
In the following diagram, those entities are described as follows:

- **4 processes** (P0, P1, P2, P3)
- **25 events** (instructions or messages)
    - **5 instruction** (block circles)
    - **20 messages** (arrorws)
        - 10 message **send**
        - 10 message **received**

![](./img/vector_clock_exampleA.png)

`VectorClockTimestampSolver#solve()` return a dictonary as a result, whose keys are each processes and values are lists of Vector Clock timestamps at each events accordingly.

```py
solver = VectorClockTimestampSolver(logger, processes)
result = solver.process()
```

In other words, the list of timestamps for P0 is as follows:

```py
processed[p0] == [
    [1, 0, 0, 0],
    [2, 2, 0, 0],
    [3, 5, 2, 0],
    [4, 5, 2, 0],
    [5, 5, 2, 0],
]
```

Each processes and events are described as `Process` and `Event` class. For full examples, please have a look at `vectorclock_test.py` unit test cases.

```py
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
processes = [p0]
```

`VectorClockTimestampSolver#print()` prints out the data model of processes and events. For example, the following is the output of `print()` for the same example.

```txt
P0 [(M1_SEND), (M3_RECV), (M5_RECV), (INST), (M8_SEND)]
P1 [(INST), (M3_SEND), (M2_RECV), (M4_SEND), (M5_SEND), (INST), (M7_SEND), (M10_RECV)]
P2 [(M1_RECV), (M2_SEND), (M6_SEND), (INST), (M8_RECV), (M9_SEND), (M4_RECV)]
P3 [(INST), (M7_RECV), (M6_RECV), (M9_RECV), (M10_SEND)]
```

When `DEBUG` log level is enabled, the solver prints out each processed events with updated timestamps. It is useful for debugging and also for tracking to understand the algorithm.

```txt
Handling P0 (M1_SEND) t=[0, 0, 0, 0]...
M1 sent with value=[1, 0, 0, 0]
Handling P0 (M3_RECV) t=[1, 0, 0, 0]...
M3 is not sent, should wait
Handling P1 (INST) t=[0, 0, 0, 0]...
instruction executed
Handling P1 (M3_SEND) t=[0, 1, 0, 0]...
M3 sent with value=[0, 2, 0, 0]
Handling P1 (M2_RECV) t=[0, 2, 0, 0]...
M2 is not sent, should wait
Handling P2 (M1_RECV) t=[0, 0, 0, 0]...
```

### Lamport Timestamp

Likewise, Lamport Timestamp can be simulated as follows.

![](./img/lamport_exampleA.png)

The above diagram is the same timelines with the example shown in the Vector Clock section, but this time timestamps are Lamport Timestamp.

```py
solver = LamportTimestampSolver(logger, processes)
result = solver.process()
```

The result for P0 is as follows:

```py
processed[p0] == [1, 3, 7, 8, 9]
```

For full examples, please have a look at `lamport_timestamps_test.py` unit test cases.
