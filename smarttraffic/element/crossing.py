from time import sleep

from smarttraffic.element import road, trafficlight


class CrossingRoad():

    def __init__(self, target_road: road.Road):
        self._lights = []
        self._cross = []
        self._road = target_road
        self._light = None

    def link_traffic_light(self, traffic_light: trafficlight.TrafficLight):
        self._light = traffic_light

    def request_close(self):
        if self._light is not None:
            if self._light.currentState is not trafficlight.TrafficState.CLOSED:
                self._light.modifyNext(
                    trafficlight.TrafficState.CLOSING, 5)

    def request_open(self):
        for cross_road in self._cross:
            cross_road.request_close()

        if self._light is not None:
            if self._light.currentState is not trafficlight.TrafficState.OPEN:
                self._light.modifyNext(
                    trafficlight.TrafficState.OPENING, 8)

    def add_cross(self, cross_road):
        self._cross.append(cross_road)


class Crossing():

    _roads = []

    def add_road(self, target_road: CrossingRoad):
        self._roads.append(target_road)

    def add_cross(self, road_a: CrossingRoad, road_b: CrossingRoad):
        road_a.add_cross(road_b)
        road_b.add_cross(road_a)
