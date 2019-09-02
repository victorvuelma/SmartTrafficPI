from enum import Enum
from datetime import datetime

from termcolor import cprint

from smarttraffic.device import trafficlight_device
from smarttraffic.manager import task_manager, network_manager


class TrafficState(Enum):
    NONE = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3
    OPENING = 4

    def stateLight(self):
        if self is TrafficState.NONE:
            return trafficlight_device.Light.NONE
        elif self is TrafficState.OPEN:
            return trafficlight_device.Light.GREEN
        elif self is TrafficState.CLOSED:
            return trafficlight_device.Light.RED
        else:
            return trafficlight_device.Light.YELLOW


class TrafficLightPhase:

    def __init__(self, state: TrafficState, duration=1.0,
                 nextPhase=None):
        self.state = state
        self.duration = duration
        self.next = nextPhase


class TrafficLightMode(Enum):
    YELLOW = 0
    DEFAULT = 1


def buildYellowBlinkPhases():
    yellow = TrafficLightPhase(TrafficState.CLOSING, 5.0)
    none = TrafficLightPhase(TrafficState.NONE, 2.0, yellow)
    yellow.next = none

    return [yellow, none]


def buildDefaultPhases():
    opening = TrafficLightPhase(TrafficState.OPENING, 3)
    closed = TrafficLightPhase(TrafficState.CLOSED, None, opening)
    closing = TrafficLightPhase(TrafficState.CLOSING, 3, closed)
    open = TrafficLightPhase(TrafficState.OPEN, None, closing)
    opening.next = open

    return [opening, closed, closing, open]


class TrafficLight:

    def __init__(self, id, mode=TrafficLightMode.YELLOW):
        super().__init__()
        self.id = id

        self.changeState(TrafficState.NONE)

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
            self.device.change_light(self.currentPhase.state.stateLight())

    def changePhases(self, phases: []):
        self.phases = phases

        self.changePhase(phases[0])

    def changePhase(self, phase: TrafficLightPhase):

        self.currentPhase = phase
        self.phaseTime = datetime.now().timestamp()

        self.nextPhase = phase.next

        if self.currentPhase.duration is not None:
            self.nextPhaseTime = self.phaseTime + self.currentPhase.duration
        else:
            self.nextPhaseTime = None

        self.changeState(self.currentPhase.state)

    def changeState(self, state: TrafficState):
        self.currentState = state

        self.updateDevice()

    def modifyNext(self, state: TrafficState, time):
        for phase in self.phases:
            if phase.state is state:

                nextTime = datetime.now().timestamp() + time

                if self.nextPhaseTime is None or nextTime < self.nextPhaseTime:
                    self.nextPhaseTime = nextTime

                self.nextPhase = phase
                break


class TrafficLightTask(task_manager.Task):

    def __init__(self, light: TrafficLight):
        super().__init__(f'trafficlight/{light.id}', 1, True)
        self.light = light

    def execute(self):
        if self.light.nextPhase is not None:
            if self.light.nextPhaseTime is not None:
                now = datetime.now().timestamp()
                if now > self.light.nextPhaseTime:

                    next = self.light.nextPhase

                    cprint(
                        f'[TRAFFICLIGHT/{self.light.id}] Change state to {next.state}.',
                        ('yellow' if next.state is TrafficState.NONE else next.state.stateLight().name.lower()))

                    network_manager._manager.send_payload('trafficlight', {
                        id: self.light.id,
                        next: next.state
                    })

                    self.light.changePhase(next)
