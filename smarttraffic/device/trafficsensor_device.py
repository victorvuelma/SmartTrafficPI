from enum import Enum


from smarttraffic.device import device
from smarttraffic.manager.device_manager import _manager as device_manager


class TrafficSensorDevice(device.Device):

    def __init__(self, slug, pin):
        self._pin = pin

        super().__init__(self, slug)

    def _setup(self):
        device_manager.pin_setup_pulldown(self._pin)

    def _hard_test(self):
        self._device_print('Place some material on sensor...')

        while True:
            if self.find():
                self._device_print('Sensor is working...')
                break

    def pins(self):
        return [self._pin]

    def find(self):
        return device_manager.pin_input(self._pin) == 1
