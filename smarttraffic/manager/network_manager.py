from enum import Enum
from os import getenv
from base64 import b64decode, b64encode
from datetime import datetime
import json

from paho.mqtt import client as mqttClient
from termcolor import cprint

from smarttraffic.manager import manager


class NetworkState(Enum):
    WAITING = 0
    CONNECTED = 1
    CLOSED = 2


class NetworkUtil():

    @staticmethod
    def encode_payload(msg={}):
        data = json.dumps(msg)
        data = data.encode('utf-8')
        data = b64encode(data)

        return data

    @staticmethod
    def decode_payload(data):
        msg = b64decode(data)
        msg = eval(msg)

        return msg


class NetworkManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self.client = None
        self.network_state = NetworkState.WAITING
        self.listeners = {}

    def init_manager(self):
        self.open_mqtt()

    def end_manager(self):
        self.close_mqtt()

    def send_mqtt(self):
        pass

    def receive_message(self, client, user, message):
        payload = NetworkUtil.decode_payload(message.payload)
        channel = message.topic

        cprint(f'[NETWORK -> {channel}]: {payload}', 'yellow')

        if(channel in self.listeners):
            listener = self.listeners[channel]
            listener(payload, client)

    def open_mqtt(self):
        if(self.network_state is not NetworkState.CONNECTED):

            MQTT_USER = getenv('MQTT_USER')
            MQTT_PASS = getenv('MQTT_PASS')
            MQTT_HOST = getenv('MQTT_HOST')
            MQTT_PORT = int(getenv('MQTT_PORT'))

            cprint('[MANAGER/network] Connecting to MQTT...', 'yellow')

            self.client = mqttClient.Client()
            self.client.on_message = self.receive_message

            self.client.username_pw_set(MQTT_USER, password=MQTT_PASS)
            self.client.connect(MQTT_HOST, port=MQTT_PORT)

            self.client.loop_start()

            self.network_state = NetworkState.CONNECTED
            cprint('[MANAGER/network] Connected to MQTT.', 'green')

    def close_mqtt(self):
        if(self.network_state is NetworkState.CONNECTED):
            self.client.loop_stop()

            self.client.disconnect()
            self.network_state = NetworkState.CLOSED

            cprint('[MANAGER/network] Disconnected from MQTT.', 'red')

    def send_payload(self, channel, payload={}):
        if(not "time" in payload):
            payload["time"] = datetime.now().timestamp()

        if(self.network_state is NetworkState.CONNECTED):
            self.client.publish(f'st/{channel}',
                                payload=NetworkUtil.encode_payload(payload))

    def listen(self, channel, listener):
        channel = f'st/{channel}'

        if(self.network_state is NetworkState.CONNECTED):
            self.client.subscribe(channel)

        self.listeners[channel] = listener

        cprint(f'[MANAGER/network] Start listen at {channel}', 'green')


_manager = NetworkManager()
