import random

from smarttraffic.device import trafficlight

class Road():

    _uuid = hash(random.getrandbits(128))
    name = None

    def __init__(self, name):
        self.name = name
        print(f'[ROAD {self._uuid}] Created with name {self.name}')

class TwoWaysRoad():

    _uuid = hash(random.getrandbits(128))
    name = None
    way_a = None
    way_b = None

    def __init__(self, name):
        self.name = name
        self.way_a = Road(f'{name} A')
        self.way_b = Road(f'{name} B')
        print(f'[ROAD TW {self._uuid}] Created a with name {self.name}')