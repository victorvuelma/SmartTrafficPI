from enum import Enum
from datetime import datetime

from termcolor import cprint

from smarttraffic.device import trafficsensor_device
from smarttraffic.manager import task_manager, network_manager, traffic_manager


class TrafficSensorState(Enum):
    NONE = 0
    ACTIVE = 1


class TrafficSensor:

    def __init__(self, slug, distance):
        super().__init__()
        self.slug = slug

        self.device = None

        self.distance = distance

        self.state = None
        self.state_time = 0

        self.change_state(TrafficSensorState.NONE)

        self.task = TrafficSensorTask(self)
        task_manager._manager.create_task(self.task)
        task_manager._manager.start_task(self.task.slug)

        traffic_manager._manager.light_register(self)

    def detect(self):
        if self.device is not None:
            return self.device.find()

    def device_link(self, device: trafficsensor_device.TrafficSensorDevice):
        self.device = device

        self.device_update()

    def change_state(self, state):
        last_state_duration = datetime.now().timestamp() - self.state_time

        last_state = self.state

        self.state = state
        self.state_time = datetime.now().timestamp()

        return last_state_duration, last_state

    def calc_velocity(self, time):
        return self.distance / time


class TrafficSensorTask(task_manager.Task):

    def __init__(self, sensor: TrafficSensor):
        super().__init__(f'ts/{sensor.slug}/main', 0.01, True)
        self.sensor = sensor

    def execute(self):
        if self.sensor.state == TrafficSensorState.NONE:
            if self.sensor.detect():
                self.sensor.change_state(TrafficSensorState.ACTIVE)
                print('find car')
        else:
            while self.sensor.detect():
                pass

            print('bye car :(')
            last_state_duration = self.sensor.change_state(TrafficSensorState.NONE):

            velocity = self.sensor.calc_velocity(last_time_duration)

            cprint(f'[TRAFFICSENSOR/{self.sensor.slug}] Traffic - Velocity: {velocity} - Time: {last_state_duration}')

            network_manager._manager.send_payload('traffic_sensor', {
                "slug": self.sensor.slug,
                "time": last_state_duration,
                "velocity": velocity
            })
