import time

from smarttraffic.device import trafficlight, pedestrianlight, trafficsensor
from smarttraffic.manager import device, system
from smarttraffic.element import road
from smarttraffic.element import crossing

def init():
    system.manager.init()

    loadSys()
    
def loadSys():
    sensor_bela_cintra = trafficsensor.TrafficSensorDevice(4)
    sensor_paulista_a = trafficsensor.TrafficSensorDevice(3)
    sensor_paulista_b = trafficsensor.TrafficSensorDevice(2)

    light_paulista_a = trafficlight.TrafficLightDevice(14, 15, 18)
    light_paulista_b = trafficlight.TrafficLightDevice(25, 8, 7)
    light_bela_cintra = trafficlight.TrafficLightDevice(16, 20, 21)
    
    device.manager.link_device(light_paulista_a)
    device.manager.link_device(light_paulista_b)
    device.manager.link_device(light_bela_cintra)
    device.manager.link_device(sensor_bela_cintra)
    device.manager.link_device(sensor_paulista_a)
    device.manager.link_device(sensor_paulista_b)

    device.manager.init()

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

    cross_paulista_bela_cintra.add_cross(cross_road_av_paulista_a, cross_road_bela_cintra)
    cross_paulista_bela_cintra.add_cross(cross_road_av_paulista_b, cross_road_bela_cintra)

    while(True):
       
        if sensor_bela_cintra.find():
            print('open bela cintra')
            cross_road_bela_cintra.request_open()

            device.manager.test_devices()
        elif sensor_paulista_a.find():
            print('open paulista a')
            cross_road_av_paulista_a.request_open()
        elif sensor_paulista_b.find():
            print('open paulista b')
            cross_road_av_paulista_b.request_open()