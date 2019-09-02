from time import sleep

from termcolor import cprint

from smarttraffic.manager import manager
from smarttraffic.device import device


class DeviceManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self._devices = []

    def init_manager(self):
        self.setup_devices()

    def start_manager(self):
        self.init_devices()

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

    def link_device(self, target_device: device.Device):
        self._devices.append(target_device)

    def setup_devices(self):
        cprint(f'[MANAGER/device] Setup all devices...', 'green')
        for target_device in self._devices:
            self.setup_device(target_device)

    def setup_device(self, target_device: device.Device):
        if(target_device.state is device.State.WAITING):
            target_device.setup_device()

    def init_devices(self):
        cprint(f'[MANAGER/device] Init all devices...', 'green')
        for target_device in self._devices:
            self.init_device(target_device)

    def init_device(self, target_device: device.Device):
        if(target_device.state is device.State.SETUP):
            target_device.init_device()


_manager = DeviceManager()
