from abc import ABC, abstractmethod
from enum import Enum

class Manager(ABC):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def end(self):
        pass

class State(Enum):
    NONE = 0
    RUNNING = 1
    STOPPED = 2
    ENDED = 3