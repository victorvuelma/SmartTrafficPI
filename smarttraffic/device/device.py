import random
from enum import Enum

class State(Enum):
    
    WAITING = 0
    SETUP = 1
    RUNNING = 2
    DISABLED = 3

class Device(object):

    def __init__(self, device, id):
        self._uuid = hash(random.getrandbits(128))
        self.id = id
        self.state = State.WAITING
        print(f'[DEVICE {self._uuid}] Created a {device.__class__.__name__}')

    def _init(self):
        pass

    def _setup(self):
        pass

    def pins(self):
        pass

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

