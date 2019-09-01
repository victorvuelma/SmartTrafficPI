import threading
from time import sleep
from enum import Enum

from termcolor import cprint

from smarttraffic.manager import manager


class TaskState(Enum):
    WAITING = 0
    START = 1
    RUNNING = 2
    STOP = 3
    STOPPING = 4
    ENDED = 5


class Task(threading.Thread):

    def __init__(self, id, delay=10, reapeating=True):
        super().__init__()
        self.id = id
        self.delay = delay
        self.repeating = reapeating
        self.state = TaskState.WAITING

    def run(self):
        while(self.state is TaskState.WAITING):
            pass

        if self.repeating:
            while self.state is not TaskState.STOP:
                if self.state is not TaskState.STOP:
                    s = self.delay
                    while s > 0 and self.state is not TaskState.STOP:
                        sleep(1)
                        s = s - 1
                self.state = TaskState.RUNNING
                self.execute()
        else:
            if self.delay is not None:
                s = self.delay
                while s > 0 and self.state is not TaskState.STOP:
                    sleep(1)
                    s = s - 1
            if self.state is not TaskState.STOP:
                self.state = TaskState.RUNNING
                self.execute()
                self.state = TaskState.STOPPING

        self.state = TaskState.ENDED

    def execute(self):
        pass


class TaskManager(manager.Manager):

    def __init__(self):
        super().__init__()
        self.tasks = {}

    def start_manager(self):
        pass

    def stop_manager(self):
        for task in self.tasks:
            task.state = TaskState.STOP

        cprint('[THREAD Manager] Waiting for all threads end...', 'yellow')
        for t in self.tasks:
            if t.state is not TaskState.ENDED:
                t.join()

        sleep(1)
        cprint('[THREAD Manager] All threads ended', 'yellow')

    def find_task(self, taskId):
        return self.tasks[taskId]

    def create_task(self, task: Task):
        self.end_task(task.id)

        self.tasks[task.id] = task

        if self.state is manager.State.RUNNING:
            self.start_task(task.id)

    def start_task(self, taskId):
        if taskId in self.tasks:
            task = self.tasks[taskId]

            if task.state is not TaskState.RUNNING and task.state is not TaskState.STOPPING:
                task.state = TaskState.START
                task.start()

                cprint(f'[TASK] Started task {taskId}.', 'green')

        else:
            cprint(f'[TASK] Try to start task {taskId}, not found.', 'red')

    def end_task(self, taskId):
        if taskId in self.tasks:
            task = self.tasks[taskId]

            if task.state is TaskState.START or task.state is TaskState.RUNNING:
                task.STATE = TaskState.STOP
                task.join()


task_manager = TaskManager()
