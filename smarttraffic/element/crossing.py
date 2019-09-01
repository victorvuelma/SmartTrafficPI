from time import sleep

from smarttraffic.element import road
from smarttraffic.device import trafficlight


class CrossingRoad():

    def __init__(self, target_road: road.Road):
        self._lights = []
        self._cross = []
        self._road = target_road

    def link_traffic_light(self, target_light: trafficlight.TrafficLightDevice):
        self._lights.append(target_light)

    def request_close(self):
        sleep(0.5)

        for target_light in self._lights:
            if(target_light._light is trafficlight.Light.GREEN):
                target_light.change_light(trafficlight.Light.YELLOW)

        sleep(1)

        for target_light in self._lights:
            if(target_light._light is trafficlight.Light.YELLOW):
                target_light.change_light(trafficlight.Light.RED)

    def request_open(self):
        for cross_road in self._cross:
            cross_road.request_close()

        for target_light in self._lights:
            target_light.change_light(trafficlight.Light.GREEN)

    def add_cross(self, cross_road):
        self._cross.append(cross_road)


class Crossing():

    _roads = []

    def add_road(self, target_road: CrossingRoad):
        self._roads.append(target_road)

    def add_cross(self, road_a: CrossingRoad, road_b: CrossingRoad):
        road_a.add_cross(road_b)
        road_b.add_cross(road_a)
