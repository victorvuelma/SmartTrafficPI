from time import sleep
from os import getenv
from datetime import datetime, timedelta

from gpiozero import CPUTemperature, LoadAverage
from termcolor import cprint

from smarttraffic.manager import manager, task_manager


class SystemMonitorTask(task_manager.Task):

    def __init__(self, id):
        super().__init__(id, 15, True)

    def execute(self):
        _manager.send_monitor()


class SystemManager(manager.Manager):

    def __init__(self):
        super().__init__()

    def init_manager(self):
        self.init_monitor()

    def start_manager(self):
        self.started = datetime.now()

        self.start_monitor()

    def end_manager(self):
        self.end_monitor()

    def init_monitor(self):
        task_manager._manager.create_task(SystemMonitorTask('system_monitor'))

    def start_monitor(self):
        task_manager._manager.start_task('system_monitor')

    def end_monitor(self):
        task_manager._manager.end_task('system_monitor')

    def td_format(self, td_object):
        seconds = int(td_object.total_seconds())
        periods = [
            ('y',        60*60*24*365),
            ('M',       60*60*24*30),
            ('d',         60*60*24),
            ('h',        60*60),
            ('m',      60),
            ('s',      1)
        ]

        strings = []
        for period_name, period_seconds in periods:
            if seconds > period_seconds:
                period_value, seconds = divmod(seconds, period_seconds)
                strings.append("%s%s" % (period_value, period_name))
        if strings.__len__ == 0:
            return '1s'

        return "".join(strings)

    def send_monitor(self):
        cprint('[SYSTEM MGR] Current system status:', 'yellow')

        now = datetime.now()
        running = now - self.started
        running = self.td_format(running)

        if(getenv('raspberry') == True):
            _cpu = CPUTemperature()
            _load = LoadAverage()
            cprint('[CPU Temperature] %0.2f ºC' % (_cpu.temperature), 'red')
            cprint(f'[LOAD] {_load.load_average}', 'green')

        cprint(f'[TIME] Running for {running}', 'yellow')


_manager = SystemManager()
