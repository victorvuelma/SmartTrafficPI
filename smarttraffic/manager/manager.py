from enum import Enum
class Manager(object):

    def __construct__(self):
        self.state = State.WAITING

    def init(self):
        if(self.state is State.WAITING):
            self.init_manager()

        if(self.state is State.WAITING or self.state is State.STOPPED ):
            self.end_manager()
            self.state = State.RUNNING

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
    RUNNING = 1
    STOPPED = 2
    ENDED = 3