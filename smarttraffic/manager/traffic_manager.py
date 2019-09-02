from enum import Enum
from os import getenv
from base64 import b64decode, b64encode
from datetime import datetime
import json

from paho.mqtt import client as mqttClient
from termcolor import cprint

from smarttraffic.manager import manager
from smarttraffic.manager.network_manager import _manager as network_manager
from smarttraffic.element import trafficlight


class TrafficManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self.lights = {}

    def init_manager(self):
        self.listen_mqtt()

    def listen_mqtt(self):
        pass

    def register(self, trafficLight: trafficlight.TrafficLight):
        self.lights[trafficLight.slug] = trafficLight


_manager = TrafficManager()
