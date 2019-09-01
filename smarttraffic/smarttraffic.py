import time
from os import getenv

from termcolor import cprint

from smarttraffic.device import trafficlight_device, pedestrianlight_device, trafficsensor_device
from smarttraffic.manager.device_manager import _manager as device_manager
from smarttraffic.manager.network_manager import _manager as network_manager
from smarttraffic.manager.system_manager import _manager as system_manager
from smarttraffic.manager.task_manager import _manager as task_manager

from smarttraffic.element import road, crossing, trafficlight

from dotenv import load_dotenv
load_dotenv()


def init():
    cprint('ST => HELLO WORLD!', 'green')

    cprint('ST => Initializing...', 'yellow')
    task_manager.init()
    system_manager.init()
    network_manager.init()
    cprint('ST => Init complete.', 'green')

    cprint('ST => Starting...', 'yellow')
    task_manager.start()
    system_manager.start()
    network_manager.start()
    cprint('ST => Start complete.', 'green')

    light = trafficlight.TrafficLight('test',
                                      trafficlight.TrafficLightMode.DEFAULT)

    if(getenv('raspberry') == True):
        loadSys()


def loadSys():
    sensor_bela_cintra = trafficsensor_device.TrafficSensorDevice(
        'bela_cintra', 4)
    sensor_paulista_a = trafficsensor_device.TrafficSensorDevice(
        'paulista_a', 3)
    sensor_paulista_b = trafficsensor_device.TrafficSensorDevice(
        'paulista_b', 2)

    light_paulista_a = trafficlight_device.TrafficLightDevice(
        'paulista_a', 14, 15, 18)
    light_paulista_b = trafficlight_device.TrafficLightDevice(
        'paulista_b', 25, 8, 7)
    light_bela_cintra = trafficlight_device.TrafficLightDevice(
        'bela_cintra', 16, 20, 21)

    device_manager.link_device(light_paulista_a)
    device_manager.link_device(light_paulista_b)
    device_manager.link_device(light_bela_cintra)
    device_manager.link_device(sensor_bela_cintra)
    device_manager.link_device(sensor_paulista_a)
    device_manager.link_device(sensor_paulista_b)

    device_manager.init()

    cross_paulista_bela_cintra = crossing.Crossing()

    road_av_paulista = road.TwoWaysRoad('Av. Paulista')
    road_bela_cintra = road.Road('Rua Bela Cintra')

    cross_road_bela_cintra = crossing.CrossingRoad(road_bela_cintra)
    cross_road_bela_cintra.link_traffic_light(light_bela_cintra)

    cross_road_av_paulista_a = crossing.CrossingRoad(road_av_paulista.way_a)
    cross_road_av_paulista_a.link_traffic_light(light_paulista_a)

    cross_road_av_paulista_b = crossing.CrossingRoad(road_av_paulista.way_b)
    cross_road_av_paulista_b.link_traffic_light(light_paulista_b)

    cross_paulista_bela_cintra.add_road(cross_road_bela_cintra)
    cross_paulista_bela_cintra.add_road(cross_road_av_paulista_a)

    cross_paulista_bela_cintra.add_cross(
        cross_road_av_paulista_a, cross_road_bela_cintra)
    cross_paulista_bela_cintra.add_cross(
        cross_road_av_paulista_b, cross_road_bela_cintra)

    while(True):
        if sensor_bela_cintra.find():
            print('open bela cintra')
            cross_road_bela_cintra.request_open()

            device.device_manager.test_devices()
        elif sensor_paulista_a.find():
            print('open paulista a')
            cross_road_av_paulista_a.request_open()
        elif sensor_paulista_b.find():
            print('open paulista b')
            cross_road_av_paulista_b.request_open()
