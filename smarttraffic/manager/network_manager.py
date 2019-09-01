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
        data = str(msg).encode('utf-8')
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
        self.state = NetworkState.WAITING
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

        cprint(f'[{channel}] -> {payload}', 'yellow')

        if(channel in self.listeners):
            listener = self.listeners[channel]
            listener(payload, client)

    def open_mqtt(self):
        if(self.state is not NetworkState.CONNECTED):

            MQTT_USER = getenv('MQTT_USER')
            MQTT_PASS = getenv('MQTT_PASS')
            MQTT_HOST = getenv('MQTT_HOST')
            MQTT_PORT = int(getenv('MQTT_PORT'))

            cprint('[NETWORK] Connecting to MQTT...', 'yellow')

            self.client = mqttClient.Client()
            self.client.on_message = self.receive_message

            self.client.username_pw_set(MQTT_USER, password=MQTT_PASS)
            self.client.connect(MQTT_HOST, port=MQTT_PORT)

            self.client.loop_start()

            self.state = NetworkState.CONNECTED
            cprint('[NETWORK] Connected to MQTT.', 'green')

    def close_mqtt(self):
        if(self.state is NetworkState.CONNECTED):
            self.client.disconnect()
            self.state = NetworkState.CLOSED

            cprint('[NETWORK] Disconnected from MQTT.', 'red')

    def send_payload(self, channel, payload={}):
        if(not 'time' in payload):
            payload['time'] = datetime.now().timestamp()

        if(self.state is NetworkState.CONNECTED):
            self.client.publish(f'st/{channel}',
                                NetworkUtil.encode_payload(payload))

    def listen(self, channel, listener):
        channel = f'st/{channel}'

        if(self.state is NetworkState.CONNECTED):
            self.client.subscribe(channel)

        self.listeners[channel] = listener

        cprint(f'[NETWORK] Start listen at {channel}', 'green')


_manager = NetworkManager()
