from enum import Enum
from datetime import datetime

from termcolor import cprint

from smarttraffic.device import trafficlight_device
from smarttraffic.manager import task_manager, network_manager


class TrafficState(Enum):
    NONE = trafficlight_device.Light.NONE
    OPEN = trafficlight_device.Light.GREEN
    CLOSING = trafficlight_device.Light.YELLOW
    CLOSED = trafficlight_device.Light.RED
    OPENING = trafficlight_device.Light.YELLOW


class TrafficLightPhase:

    def __init__(self, state: TrafficState, duration=1.0,
                 next=None):
        self.state = state
        self.duration = duration
        self.next = next


class TrafficLightMode(Enum):
    YELLOW = 0
    DEFAULT = 1


def buildYellowBlinkPhases():
    yellow = TrafficLightPhase(TrafficState.CLOSING, 5.0)
    none = TrafficLightPhase(TrafficState.NONE, 2.0, yellow)
    yellow.next = none

    return [yellow, none]


def buildDefaultPhases(greenDuration=20, redDuration=20):
    opening = TrafficLightPhase(TrafficState.OPENING, 3)
    closed = TrafficLightPhase(TrafficState.CLOSED, redDuration, opening)
    closing = TrafficLightPhase(TrafficState.CLOSING, 3, closed)
    green = TrafficLightPhase(TrafficState.OPEN, greenDuration, closing)
    opening.next = green

    return [opening, closed, closing, green]


class TrafficLight:

    def __init__(self, id, mode: TrafficLightMode):
        super().__init__()
        self.id = id

        self.changeMode(mode)

        self.task = TrafficLightTask(self)
        task_manager._manager.create_task(self.task)
        task_manager._manager.start_task(self.task.id)

    def changeMode(self, mode: TrafficLightMode):
        if(mode is TrafficLightMode.YELLOW):
            self.changePhases(buildYellowBlinkPhases())
        elif(mode is TrafficLightMode.DEFAULT):
            self.changePhases(buildDefaultPhases())

    def linkDevice(self, device: trafficlight_device.TrafficLightDevice):
        self.device = device

        self.updateDevice()

    def updateDevice(self):
        if hasattr(self, 'device'):
            self.device.change_light(self.currentPhase.state)

    def changePhases(self, phases: []):
        self.phases = phases

        self.changePhase(phases[0])

    def changePhase(self, phase: TrafficLightPhase):

        self.currentPhase = phase
        self.phaseTime = datetime.now().timestamp()

        self.nextPhase = phase.next
        self.nextPhaseTime = self.phaseTime + self.currentPhase.duration

        self.updateDevice()


class TrafficLightTask(task_manager.Task):

    def __init__(self, light: TrafficLight):
        super().__init__(f'trafficlight/{light.id}', 1, True)
        self.light = light

    def execute(self):
        if self.light.nextPhase is not None:
            now = datetime.now().timestamp()
            if now > self.light.nextPhaseTime:

                cprint(f'[TRAFFICLIGHT/{self.light.id}] Change state to {self.light.nextPhase.state}.',
                       self.light.nextPhase.state.value.name.lower())

                network_manager._manager.send_payload('trafficlight', {
                    id: self.light.id,
                    next: self.light.nextPhase.state
                })

                self.light.changePhase(self.light.nextPhase)
