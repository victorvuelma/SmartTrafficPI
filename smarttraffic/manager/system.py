import multitasking
from gpiozero import CPUTemperature
from time import sleep

from smarttraffic.manager import manager


class SystemManager(manager.Manager):

    def __init__(self):
        pass

    def init(self):
        self.startMonitor()

    def end(self):
        pass

    @multitasking.task
    def startMonitor(self):
        self._runMonitor = True

        while(self._runMonitor):
            self.sendMonitor()
            
            if(self._runMonitor): sleep(15)
            
    def endMonitor(self):
        self._runMonitor = False

    def sendMonitor(self):
        _cpu = CPUTemperature()

        print('[SYSTEM MGR] Current system status:')
        print(f'[CPU] Temperature: {_cpu.temperature}')

manager = SystemManager()        