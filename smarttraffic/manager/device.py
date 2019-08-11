from time import sleep

from smarttraffic.manager import manager
from smarttraffic.device import device 

class DeviceManager(manager.Manager):

    _devices = []

    def init(self):
        self.setup_devices()

        self.init_devices()

    def end(self):
        pass

    def test_devices(self):
        confirm = input('[MGR DEVICE] Do you really want to test all devices? (Y/n) ')

        if confirm == 'Y':
            print(f'[MGR DEVICE] Testing all devices...')

            for target_device in self._devices:
                target_device.test_device()
                sleep(1)

            print(f'[MGR DEVICE] Test ended')
        else:
            print(f'[MGR DEVICE] Test cancelled')

    def link_device(self, target_device: device.Device):
        self._devices.append(target_device)

    def setup_devices(self):
        print(f'[MGR DEVICE] Setup all devices...')
        for target_device in self._devices:
            self.setup_device(target_device)

    def setup_device(self, target_device: device.Device):
        if(target_device.state is device.State.WAITING):
            target_device.setup_device()

    def init_devices(self):
        print(f'[MGR DEVICE] Init all devices...')
        for target_device in self._devices:
            self.init_device(target_device)

    def init_device(self, target_device: device.Device):
        if(target_device.state is device.State.SETUP):
            target_device.init_device()

manager = DeviceManager()