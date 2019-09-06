import random

from termcolor import cprint


class Road:

    def __init__(self, slug, name):
        self._uuid = hash(random.getrandbits(128))

        self.slug = slug
        self.name = name

        cprint(f'[ROAD/{self.slug}] Created with name {self.name}', 'green')


class TwoWaysRoad:

    def __init__(self, slug, name):
        self._uuid = hash(random.getrandbits(128))

        self.name = name
        self.slug = slug

        self.way_a = Road(f'{slug}_a', f'{name} A')
        self.way_b = Road(f'{slug}_b', f'{name} B')

        cprint(
            f'[ROAD/TW/{self.slug}] Created a with name {self.name}', 'green')

    def way_roads(self):
        return [self.way_a, self.way_b]
