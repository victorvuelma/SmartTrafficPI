from enum import Enum
from gpiozero import LED

from smarttraffic.device import device

class Light(Enum):

    NONE = 0
    RED = 1
    GREEN = 2

class PedestrianLightDevice(device.Device):

    def __init__(self, _pin_led_r, _pin_led_g):
        super().__init__(self)
        self._light = Light.NONE
        self._pin_led_r = _pin_led_r
        self._pin_led_g = _pin_led_g

    def _setup(self):
        self._led_g = LED(self._pin_led_g)
        self._led_r = LED(self._pin_led_r)

    def _init(self):
        self.change_light(Light.RED)

    def pins(self):
        return [ self._pin_led_r, self._pin_led_g ]


    def change_light(self, light: Light):
        if(self.state is device.State.RUNNING):
            current = self._find_led(self._light)
            if(current is not None): current.off()

            self._light =  light   

            led = self._find_led(self._light)
            if(led is not None): led.on()
        else:
            self._device_print(f'Cant light at state {self.state}')

    def _find_led(self, light: Light):
        if(light is Light.RED): return self._led_r
        elif(light is Light.GREEN): return self._led_g
        return None
