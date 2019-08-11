from enum import Enum
from gpiozero import Button

from smarttraffic.device import device

class TrafficSensorDevice(device.Device):

    def __init__(self, pin):
        super().__init__(self)
        self._pin = pin
        self._sensor = None

    def _setup(self):
        self._sensor = Button(self._pin)

    def _init(self):
        pass

    def pins(self):
        return [ self._pin ]

    def find(self):
        return self._sensor.is_pressed

    def _hard_test(self):
        self._device_print('Place some material on sensor...')

        while(True):
            print(self.find())
            if self.find():
            
                break