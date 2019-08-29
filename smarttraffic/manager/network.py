from enum import Enum
from os import getenv

from paho.mqtt import client as mqttClient
from termcolor import cprint

from smarttraffic.manager import manager


class NetworkState(Enum):
    WAITING = 0
    CONNECTED = 1
    CLOSED = 2


class NetworkManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self.client = None
        self.state = NetworkState.WAITING

    def init_manager(self):
        self.open_mqtt()

    def end_manager(self):
        self.close_mqtt()

    def send_mqtt(self):
        pass

    def open_mqtt(self):
        if(self.state is not NetworkState.CONNECTED):

            MQTT_USER = getenv('MQTT_USER')
            MQTT_PASS = getenv('MQTT_PASS')
            MQTT_HOST = getenv('MQTT_HOST')
            MQTT_PORT = int(getenv('MQTT_PORT'))

            cprint('[NETWORK] Connecting to MQTT...', 'yellow')

            self.client = mqttClient.Client()
            self.client.username_pw_set(MQTT_USER, password=MQTT_PASS)
            self.client.connect(MQTT_HOST, port=MQTT_PORT)
            self.state = NetworkState.CONNECTED

            cprint('[NETWORK] Connected to MQTT.', 'green')

    def close_mqtt(self):
        if(self.state is NetworkState.CONNECTED):
            self.client.disconnect()
            self.state = NetworkState.CLOSED


network_manager = NetworkManager()
