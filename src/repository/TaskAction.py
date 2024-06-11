# This file contains the TaskAction class which is used to store the task information and the state of the task. The class has a __call__ method which is used to set the task information and a export method which is used to export the task information in the required format. The class has the following attributes:
from datetime import datetime
import json

class TaskAction:
    task_id: str
    M1: int
    M2: int
    M3: int
    Area1: bool
    Area2: bool
    Area3: bool
    state: int = 3
    hour: int
    minute: int
    start_time: datetime
    end_time: datetime
    repeat: int = None

    
    
    def __call__(self, data):
        data = json.loads(data)
        self.task_id = data["Task_id"]
        self.M1 = data["M1"]
        self.M2 = data["M2"]
        self.M3 = data["M3"]
        self.hour = data["hour"]
        self.minute = data["minute"]
        self.Area1 = data["Area1"]
        self.Area2 = data["Area2"]
        self.Area3 = data["Area3"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.repeat = data["repeat"] if "repeat" in data else None

    def export(self):
        return {"Task_id": self.task_id, "state": self.state}
