import random

from termcolor import cprint


class Road():

    _uuid = hash(random.getrandbits(128))
    name = None

    def __init__(self, name):
        self.name = name
        cprint(f'[ROAD {self._uuid}] Created with name {self.name}', 'green')


class TwoWaysRoad():

    _uuid = hash(random.getrandbits(128))
    name = None
    way_a = None
    way_b = None

    def __init__(self, name):
        self.name = name
        self.way_a = Road(f'{name} A')
        self.way_b = Road(f'{name} B')
        cprint(
            f'[ROAD TW {self._uuid}] Created a with name {self.name}', 'green')
