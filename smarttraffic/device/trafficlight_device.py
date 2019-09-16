from enum import Enum
from time import sleep

from smarttraffic.device import device
from smarttraffic.manager.device_manager import  _manager as device_manager


class Light(Enum):

    NONE = 0
    RED = 1
    YELLOW = 2
    GREEN = 3


class TrafficLightDevice(device.Device):

    def __init__(self, slug, pin_led_r, pin_led_y, pin_led_g):
        self._light = Light.NONE
        self.pin_led_r = pin_led_r
        self.pin_led_y = pin_led_y
        self.pin_led_g = pin_led_g

        super().__init__(self, slug)

    def pins(self):
        return [self.pin_led_r, self.pin_led_y, self.pin_led_g]

    def _setup(self):
        for pin in self.pins():
            device_manager.pin_setup_output(pin)

    def _init(self):
        self.change_light(Light.RED)

    def _hard_test(self):
        for pin in self.pins():
            device_manager.pin_output(pin, False)

        for pin in self.pins():
            device_manager.pin_output(pin, True)
            sleep(0.5)
            device_manager.pin_output(pin, False)
            sleep(0.1)

    def _find_led(self, light: Light):
        if light is Light.RED:
            return self.pin_led_r
        elif light is Light.YELLOW:
            return self.pin_led_y
        elif light is Light.GREEN:
            return self.pin_led_g
        return None

    def change_light(self, light: Light):
        if self.state is device.State.RUNNING:
            current = self._find_led(self._light)
            if current is not None:
                device_manager.pin_output(current, False)

            self._light = light

            led = self._find_led(self._light)
            if led is not None:
                device_manager.pin_output(led, True)
        else:
            self._device_print(
                f'Cant change traffic light at state {self.state}')
