from enum import Enum


class Manager(object):

    def __init__(self):
        self.state = State.WAITING

    def init(self):
        if(self.state is State.WAITING):
            self.init_manager()
            self.state = State.INITIALIZED

    def start(self):
        if(self.state is State.WAITING):
            self.init_manager()

        if(self.state is State.INITIALIZED or self.state is State.STOPPED):
            self.start_manager()

    def end(self):
        if(self.state is State.RUNNING or self.state is State.STOPPED):
            self.end_manager()

    def init_manager(self):
        pass

    def start_manager(self):
        pass

    def end_manager(self):
        pass


class State(Enum):
    WAITING = 0
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3
    ENDED = 4
