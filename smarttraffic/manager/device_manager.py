from time import sleep
import RPi.GPIO as gpio

from termcolor import cprint

from smarttraffic.manager import manager
from smarttraffic.device import device


class DeviceManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self._devices = []

    def init_manager(self):
        self.setup_gpio()
        self.setup_devices()

    def start_manager(self):
        self.init_devices()

    def end_manager(self):
        self.cleanup_gpio()

    def test_devices(self):
        confirm = input(
            '[MANAGER/device] Do you really want to test all devices? (Y/n) ')

        if confirm == 'Y':
            cprint(f'[MANAGER/device] Testing all devices...', 'yellow')

            for target_device in self._devices:
                target_device.test_device()
                sleep(1)

            cprint(f'[MANAGER/device] Test ended', 'green')
        else:
            cprint(f'[MANAGER/device] Test cancelled', 'red')

    def link_device(self, target_device):
        self._devices.append(target_device)

        if self.state is manager.State.INITIALIZED or self.state is manager.State.WAITING:
            self.setup_device(target_device)

        if self.state is manager.State.WAITING:
            self.init_device(target_device)

    def cleanup_gpio(self):
        gpio.cleanup()

    def setup_gpio(self):
        gpio.setmode(gpio.BOARD)

    def setup_devices(self):
        cprint(f'[MANAGER/device] Setup all devices...', 'green')
        for target_device in self._devices:
            self.setup_device(target_device)

    def setup_device(self, target_device):
        if target_device.state is device.State.WAITING:
            target_device.setup_device()

    def init_devices(self):
        cprint(f'[MANAGER/device] Init all devices...', 'green')
        for target_device in self._devices:
            self.init_device(target_device)

    def init_device(self, target_device):
        if target_device.state is device.State.SETUP:
            target_device.init_device()

    def pin_setup_output(self, pin):
        gpio.setup(pin, gpio.OUT)

    def pin_setup_pulldown(self, pin):
        gpio.pud_down(pin)

    def pin_output(self, pin, value=False):
        if value:
            gpio.output(pin, gpio.HIGH)
        else:
            gpio.output(pin, gpio.LOW)

    def pin_input(self, pin):
        return gpio.input(pin)

_manager = DeviceManager()
