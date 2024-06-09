# This file contains the TaskAction class which is used to store the task information and the state of the task. The class has a __call__ method which is used to set the task information and a export method which is used to export the task information in the required format. The class has the following attributes:
from datetime import datetime


class TaskAction:
    task_id: string
    M1: int
    M2: int
    M3: int
    Area1: bool
    Area2: bool
    Area3: bool
    state: int = 3
    start_time: datetime
    timeout: int = None
    repeat: int = None

    def __call__(self, data):
        self.task_id = data["Task_id"]
        self.M1 = data["M1"]
        self.M2 = data["M2"]
        self.M3 = data["M3"]
        self.Area1 = data["Area1"]
        self.Area2 = data["Area2"]
        self.Area3 = data["Area3"]
        self.start_time = datetime.strptime(data["start_time"], "%Y-%m-%d %H:%M:%S")
        self.timeout = data["timeout"] if "timeout" in data else None
        self.repeat = data["repeat"] if "repeat" in data else None

    def export(self):
        return {"Task_id": self.task_id, "state": self.state}
