import time
from os import getenv

from smarttraffic.device import trafficlight, pedestrianlight, trafficsensor
from smarttraffic.manager import device, system, task, network
from smarttraffic.element import road
from smarttraffic.element import crossing

from dotenv import load_dotenv
load_dotenv()


def init():
    system.system_manager.init()

    task.task_manager.init_manager()

    network.network_manager.init_manager()

    if(getenv('raspberry') == True):
        loadSys()


def loadSys():
    sensor_bela_cintra = trafficsensor.TrafficSensorDevice('bela_cintra', 4)
    sensor_paulista_a = trafficsensor.TrafficSensorDevice('paulista_a', 3)
    sensor_paulista_b = trafficsensor.TrafficSensorDevice('paulista_b', 2)

    light_paulista_a = trafficlight.TrafficLightDevice(
        'paulista_a', 14, 15, 18)
    light_paulista_b = trafficlight.TrafficLightDevice('paulista_b', 25, 8, 7)
    light_bela_cintra = trafficlight.TrafficLightDevice(
        'bela_cintra', 16, 20, 21)

    device.device_manager.link_device(light_paulista_a)
    device.device_manager.link_device(light_paulista_b)
    device.device_manager.link_device(light_bela_cintra)
    device.device_manager.link_device(sensor_bela_cintra)
    device.device_manager.link_device(sensor_paulista_a)
    device.device_manager.link_device(sensor_paulista_b)

    device.device_manager.init()

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
