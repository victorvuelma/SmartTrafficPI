from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from termcolor import cprint

from smarttraffic.device import trafficlight_device, trafficsensor_device
from smarttraffic.element import road, crossing, trafficlight
from smarttraffic.manager.device_manager import _manager as device_manager
from smarttraffic.manager.network_manager import _manager as network_manager
from smarttraffic.manager.system_manager import _manager as system_manager
from smarttraffic.manager.task_manager import Task
from smarttraffic.manager.task_manager import _manager as task_manager
from smarttraffic.manager.traffic_manager import _manager as traffic_manager

load_dotenv()


def init():
    cprint('ST => HELLO WORLD!', 'green')

    cprint('ST => Initializing...', 'yellow')
    task_manager.init()
    system_manager.init()
    device_manager.init()
    network_manager.init()
    traffic_manager.init()
    cprint('ST => Init complete.', 'green')

    cprint('ST => Starting...', 'yellow')
    task_manager.start()
    system_manager.start()
    network_manager.start()
    traffic_manager.start()
    device_manager.start()
    cprint('ST => Start complete.', 'green')

    light_paulista_a = trafficlight.TrafficLight(
        'av_paulista_a', trafficlight.TrafficLightMode.DEFAULT)
    light_paulista_b = trafficlight.TrafficLight(
        'av_paulista_b', trafficlight.TrafficLightMode.DEFAULT)
    light_bela_cintra = trafficlight.TrafficLight(
        'rua_bela_cintra', trafficlight.TrafficLightMode.DEFAULT)

    cross_paulista_bela_cintra = crossing.Crossing()

    road_av_paulista = road.TwoWaysRoad('av_paulista', 'Av. Paulista')
    road_bela_cintra = road.Road('rua_bela_cintra', 'Rua Bela Cintra')

    cross_road_bela_cintra = crossing.CrossingRoad(road_bela_cintra)
    cross_road_bela_cintra.link_traffic_light(light_bela_cintra)

    cross_road_av_paulista_a = crossing.CrossingRoad(road_av_paulista.way_a)
    cross_road_av_paulista_a.link_traffic_light(light_paulista_a)

    cross_road_av_paulista_b = crossing.CrossingRoad(road_av_paulista.way_b)
    cross_road_av_paulista_b.link_traffic_light(light_paulista_b)

    cross_paulista_bela_cintra.add_road(cross_road_bela_cintra)
    cross_paulista_bela_cintra.add_road(cross_road_av_paulista_a)

    crossing.Crossing.add_cross(cross_road_bela_cintra, cross_road_av_paulista_a)
    crossing.Crossing.add_cross(cross_road_bela_cintra, cross_road_av_paulista_b)

    light_bela_cintra.state_next(trafficlight.TrafficState.CLOSED, 0)
    light_paulista_a.state_next(trafficlight.TrafficState.OPEN, 0)
    light_paulista_b.state_next(trafficlight.TrafficState.OPEN, 0)

    class MainTask(Task):

        def __init__(self):
            super().__init__('main', 1, True)

        def execute(self):
            now = datetime.now().timestamp()

            if light_bela_cintra.current_state is trafficlight.TrafficState.OPEN:
                duration = now - light_bela_cintra.phase_time

                if duration > 12:
                    cross_road_av_paulista_a.request_open()
                    cross_road_av_paulista_b.request_open()

            if light_paulista_a.current_state is trafficlight.TrafficState.OPEN:
                duration = now - light_paulista_a.phase_time

                if duration > 22:
                    cross_road_bela_cintra.request_open()

    task = MainTask()
    task_manager.create_task(task)
    task_manager.start_task('main')

    if getenv('RASPBERRY') == 'TRUE':
        sensor_bela_cintra = trafficsensor_device.TrafficSensorDevice(
            'bela_cintra', 3)
        sensor_paulista_a = trafficsensor_device.TrafficSensorDevice(
            'paulista_a', 5)
        sensor_paulista_b = trafficsensor_device.TrafficSensorDevice(
            'paulista_b', 7)

        device_light_bela_cintra = trafficlight_device.TrafficLightDevice(
            'bela_cintra', 8, 10, 12)
        device_light_paulista_a = trafficlight_device.TrafficLightDevice(
            'paulista_a', 22, 24, 26)
        device_light_paulista_b = trafficlight_device.TrafficLightDevice(
            'paulista_b', 36, 38, 40)

        light_bela_cintra.device_link(device_light_bela_cintra)

        light_paulista_a.device_link(device_light_paulista_a)

        light_paulista_b.device_link(device_light_paulista_b)

        while True:
            if sensor_bela_cintra.find():
                print('open bela cintra')
                cross_road_bela_cintra.request_open()
            elif sensor_paulista_a.find():
                print('open paulista a')
                cross_road_av_paulista_a.request_open()
            elif sensor_paulista_b.find():
                print('open paulista b')
                cross_road_av_paulista_b.request_open()
