from typing import Dict
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import serial
from ..config import glob_var
from ..device_wrapper import Relay, Sensor
from ..connector import AdafruitConnector
from ..tasks import read_sensors, water_fsm
from ..repository import TaskAction


def time_processing(task: TaskAction):
    return {
        # "next_run_time": task.start_time,  # Schedule time
        # "max_instances": 1,  # Assuming you want only one instance of the job at a time
        # "misfire_grace_time": task.timeout,  # Time period in seconds the scheduler allows the job to be late
        # "replace_existing": True,  # Replace existing jobs with the same ID
        # Additional parameters for repeat logic can be implemented here
        # APScheduler does not have a direct 'repeat' parameter, but you can use 'trigger' for repeating jobs
        "day_of_week": "mon-fri",
        "hour": task.start_time.hour,
        "minute": task.start_time.minute,
        "start_date": task.start_time.strftime("%Y-%m-%d"),
        "end_date": (
            task.start_time + datetime.timedelta(days=task.repeat * 7)
        ).strftime("%Y-%m-%d"),
    }


def mqtt_handler(scheduler: BackgroundScheduler):
    def handler(feed_id, payload):
        if feed_id == "task_action":
            task = TaskAction()
            task(payload)
            processed_time = time_processing(task)
            scheduler.add_job(
                water_fsm,
                "cron",
                args=[glob_var.list_actuators, task],
                id=task.task_id,
                **processed_time
            )
            glob_var.mqtt_client.publish(
                "task_result", {"Task_id": task.task_id, "state": 3}
            )

        elif feed_id == "task_result_query":
            state = scheduler.get_job(payload["Task_id"]).state
            glob_var.mqtt_client.publish(
                "task_result", {"Task_id": payload["Task_id"], "state": state}
            )

    return handler


class GeneralPipeline:
    def __init__(
        self, ser: serial.Serial, scheduler: BackgroundScheduler, config: Dict
    ):
        self.config = config
        self.serial = ser
        self.extract_sensors(config)
        # print({sensor.get_name(): sensor.read() for sensor in self.sensors})
        self.extract_actuators(config)
        self.mqtt_client = glob_var.mqtt_client
        self.scheduler = scheduler

    def setup_jobs(self):
        self.mqtt_client.addCallbackFn(mqtt_handler(self.scheduler))
        self.scheduler.add_job(
            read_sensors,
            "interval",
            args=[
                self.config["device_feed"],
            ],
            seconds=5,
        )

    def extract_sensors(self, config: Dict):
        list_device = []
        for d in config["devices"]:
            if d["type"] == "sensor":
                sensor = Sensor(
                    serial=self.serial,
                    id=d["id"],
                    name=d["name"],
                    area=d["area"],
                    register_address=d["register_address"],
                )
                list_device.append(sensor)
        glob_var.list_sensors.extend(list_device)

    def extract_actuators(self, config: Dict):
        list_device = []
        for d in config["devices"]:
            if d["type"] == "actuator":
                actuator = Relay(
                    serial=self.serial,
                    id=d["id"],
                    name=d["name"],
                    area=d["area"],
                    register_address=d["register_address"],
                    on_value=d["on_value"],
                    off_value=d["off_value"],
                )
                list_device.append(actuator)
        glob_var.list_actuators.extend(list_device)

    def run(self):
        self.setup_jobs()
        self.scheduler.start()
        print("IOT Service is running ...")
        while True:
            pass
