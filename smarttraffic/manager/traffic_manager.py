from termcolor import cprint

from smarttraffic.element import trafficlight, crossing
from smarttraffic.manager import manager
from smarttraffic.manager.network_manager import _manager as network_manager


class TrafficManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self.lights = {}
        self.crossroad = {}

    def start_manager(self):
        self.init_mqtt()

    def init_mqtt(self):
        def listen_cross(payload, channel):
            if 'slug' in payload and 'run' in payload:
                slug = payload['slug']
                run = payload['run']

                if slug in self.crossroad:
                    cross = self.crossroad[slug]
                    cprint(f'[ROAD/{slug}] Receive command for {run}.', 'red')

                    if run is 'open':
                        cross.request_open()
                    elif run is 'close':
                        cross.request_close()

        network_manager.listen('cross', listen_cross)

    def crossroad_register(self, cross_road):
        self.crossroad[cross_road.slug] = cross_road

    def light_register(self, traffic_light):
        self.lights[traffic_light.slug] = traffic_light


_manager = TrafficManager()
