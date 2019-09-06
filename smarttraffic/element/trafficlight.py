from enum import Enum
from datetime import datetime

from termcolor import cprint

from smarttraffic.device import trafficlight_device
from smarttraffic.manager import task_manager, network_manager, traffic_manager


class TrafficState(Enum):
    NONE = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3
    OPENING = 4

    def state_light(self):
        if self is TrafficState.NONE:
            return trafficlight_device.Light.NONE
        elif self is TrafficState.OPEN:
            return trafficlight_device.Light.GREEN
        elif self is TrafficState.CLOSED:
            return trafficlight_device.Light.RED
        else:
            return trafficlight_device.Light.YELLOW


class TrafficLightPhase:

    def __init__(self, state: TrafficState, duration=1.0, next_phase=None):
        self.state = state
        self.duration = duration
        self.next = next_phase


class TrafficLightMode(Enum):
    YELLOW = 0
    DEFAULT = 1


def build_yellow_blink_phases():
    yellow = TrafficLightPhase(TrafficState.CLOSING, 5.0)
    none = TrafficLightPhase(TrafficState.NONE, 2.0, yellow)
    yellow.next = none

    return [yellow, none]


def build_default_phases():
    opening_phase = TrafficLightPhase(TrafficState.OPENING, 3)
    closed_phase = TrafficLightPhase(TrafficState.CLOSED, 0, opening_phase)
    closing_phase = TrafficLightPhase(TrafficState.CLOSING, 3, closed_phase)
    open_phase = TrafficLightPhase(TrafficState.OPEN, 0, closing_phase)
    opening_phase.next = open_phase

    return [opening_phase, closed_phase, closing_phase, open_phase]


class TrafficLight:

    def __init__(self, slug, mode=TrafficLightMode.YELLOW):
        super().__init__()
        self.slug = slug

        self.device = None

        self.phases = []
        self.current_phase = None
        self.current_state = None
        self.phase_time = 0

        self.next_phase = None
        self.next_phase_time = 0

        self.state_change(TrafficState.NONE)

        self.mode_change(mode)

        self.task = TrafficLightTask(self)
        task_manager._manager.create_task(self.task)
        task_manager._manager.start_task(self.task.slug)

        traffic_manager._manager.light_register(self)

    def mode_change(self, mode: TrafficLightMode):
        if mode is TrafficLightMode.YELLOW:
            self.phases_change(build_yellow_blink_phases())
        elif mode is TrafficLightMode.DEFAULT:
            self.phases_change(build_default_phases())

    def device_link(self, device: trafficlight_device.TrafficLightDevice):
        self.device = device

        self.device_update()

    def device_update(self):
        if self.device is not None:
            self.device.change_light(self.current_phase.state.state_light())

    def phases_change(self, phases: []):
        self.phases = phases

        self.phase_change(phases[0])

    def phase_change(self, phase: TrafficLightPhase):

        self.current_phase = phase
        self.phase_time = datetime.now().timestamp()

        self.next_phase = phase.next

        if self.current_phase.duration is not 0:
            self.next_phase_time = self.phase_time + self.current_phase.duration
        else:
            self.next_phase_time = None

        self.state_change(self.current_phase.state)

    def state_change(self, state: TrafficState):
        self.current_state = state

        self.device_update()

    def state_next(self, state: TrafficState, time):
        for phase in self.phases:
            if phase.state is state:

                next_time = datetime.now().timestamp() + time

                if self.next_phase_time is None or next_time < self.next_phase_time:
                    self.next_phase_time = next_time

                self.next_phase = phase
                break


class TrafficLightTask(task_manager.Task):

    def __init__(self, light: TrafficLight):
        super().__init__(f'tl/{light.slug}/main', 1, True)
        self.light = light

    def execute(self):
        if self.light.next_phase is not None:
            if self.light.next_phase_time is not None:
                now = datetime.now().timestamp()
                if now > self.light.next_phase_time:

                    next_phase = self.light.next_phase

                    cprint(
                        f'[TRAFFICLIGHT/{self.light.slug}] Change state to {next_phase.state}.',
                        ('yellow' if
                         next_phase.state is TrafficState.NONE
                         else next_phase.state.state_light().name.lower()))

                    network_manager._manager.send_payload('traffic_light', {
                        "slug": self.light.slug,
                        "action": "change_state",
                        "state": next_phase.state.name
                    })

                    self.light.phase_change(next_phase)
