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

    def __init__(self, id, pinLedR, pinLedY, pinLedG):
        super().__init__(self, id)
        self._light = Light.NONE
        self.pinLedR = pinLedR
        self.pinLedY = pinLedY
        self.pinLedG = pinLedG

    def pins(self):
        return [ self.pinLedR, self.pinLedY, self.pinLedG ]

    def leds(self):
        return [ self.ledG, self.ledY, self.ledR ]

    def _setup(self):
        self.ledG = LED(self.pinLedG)
        self.ledR = LED(self.pinLedR)
        self.ledY = LED(self.pinLedY)

    def _init(self):
        self.change_light(Light.YELLOW)

    def _hard_test(self):
        for led in self.leds():
            led.off()

        for led in self.leds():
            led.on()
            sleep(0.5)
            led.off()
            sleep(0.1)

    def change_light(self, light: Light):
        if(self.state is device.State.RUNNING):
            current = self._find_led(self._light)
            if(current is not None): current.off()

            self._light =  light           

            led = self._find_led(self._light)
            if(led is not None): led.on()
        else:
            self._device_print(f'Cant change traffic light at state {self.state}')

    def _find_led(self, light: Light):
        if(light is Light.RED): return self.ledR
        elif(light is Light.YELLOW): return self.ledY
        elif(light is Light.GREEN): return self.ledG
        return None
