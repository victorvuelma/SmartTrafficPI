from enum import Enum
from gpiozero import LED
from time import sleep

from smarttraffic.device import device


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

    def leds(self):
        return [self.led_g, self.led_y, self.led_r]

    def _setup(self):
        self.led_g = LED(self.pin_led_g)
        self.led_r = LED(self.pin_led_r)
        self.led_y = LED(self.pin_led_y)

        print('yey, setup!')

    def _init(self):
        self.change_light(Light.RED)

    def _hard_test(self):
        for led in self.leds():
            led.off()

        for led in self.leds():
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.1)

    def _find_led(self, light: Light):
        if light is Light.RED:
            return self.led_r
        elif light is Light.YELLOW:
            return self.led_y
        elif light is Light.GREEN:
            return self.led_g
        return None

    def change_light(self, light: Light):
        if self.state is device.State.RUNNING:
            current = self._find_led(self._light)
            if current is not None:
                current.off()

            self._light = light

            led = self._find_led(self._light)
            if led is not None:
                led.on()
        else:
            self._device_print(
                f'Cant change traffic light at state {self.state}')
