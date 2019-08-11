import random
from enum import Enum

from abc import ABC, abstractmethod

class State(Enum):
    
    WAITING = 0
    SETUP = 1
    RUNNING = 2
    DISABLED = 3

class Device(ABC):

    _uuid = None
    state = State.WAITING

    def __init__(self, device):
        self._uuid = hash(random.getrandbits(128))
        print(f'[DEVICE {self._uuid}] Created a {device.__class__.__name__}')

    @abstractmethod
    def _init(self):
        pass

    @abstractmethod
    def _setup(self):
        pass

    @abstractmethod
    def pins(self):
        pass

    @abstractmethod
    def _hard_test(self):
        pass

    def _device_print(self, str):
        print(f'[DEVICE {self._uuid}] {str}')

    def _device_input(self, str):
        return input(f'[DEVICE {self._uuid}] {str}')

    def test_device(self):
        self._device_input('Waiting for ok to start test... ')
        self._hard_test()
        self._device_print('Test end')

    def setup_device(self):
        if(self.state is State.WAITING):
            self.state = State.SETUP
            self._setup()
            self._device_print(f'Done setup')
        else:
            self._device_print(f'Cant run setup at state {self.state}')

    def init_device(self):
        if(self.state is State.SETUP):
            self.state = State.RUNNING
            self._init()
            self._device_print(f'Done init')
        else:
            self._device_print(f'Cant run init at state {self.state}')

