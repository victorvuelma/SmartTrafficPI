from time import sleep
import multitasking
from gpiozero import CPUTemperature, LoadAverage
from termcolor import cprint

from smarttraffic.manager import manager
from smarttraffic.manager import task

class SystemMonitorTask(task.Task):

    def __init__(self, id):
        super().__init__(id, 15, True)

    def execute(self):
        system_manager.send_monitor()

class SystemManager(manager.Manager):

    def __init__(self):
        super().__init__()

    def init_manager(self):
        pass
    
    def start_manager(self):
        self.start_monitor()

    def end_manager(self):
        self.end_monitor()

    def start_monitor(self):
        task.task_manager.create_task(SystemMonitorTask('system_monitor'))
            
    def end_monitor(self):
        task.task_manager.end_task('system_monitor')

    def send_monitor(self):
        _cpu = CPUTemperature()
        _load = LoadAverage()

        cprint('[SYSTEM MGR] Current system status:', 'yellow')
        cprint('[CPU Temperature] %0.2f ºC' % (_cpu.temperature), 'red')
        cprint(f'[LOAD] {_load.load_average}', 'green')

system_manager = SystemManager()        