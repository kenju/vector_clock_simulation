from abc import abstractmethod


class Timestamp:
    @abstractmethod
    def incr(self, process_id: int):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def merge(self, process_id: int, other: 'Timestamp'):
        raise NotImplementedError
