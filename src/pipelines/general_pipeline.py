from typing import Dict
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
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


def mqtt_handler(
    actuators: Relay, scheduler: BackgroundScheduler, mqtt_client: AdafruitConnector
):
    def handler(feed_id, payload):
        if feed_id == "task_action":
            task = TaskAction()
            task(payload)
            processed_time = time_processing(task)
            scheduler.add_job(
                water_fsm,
                "cron",
                args=[actuators, task, mqtt_client],
                id=task.task_id,
                **processed_time
            )

        elif feed_id == "task_result_query":
            state = scheduler.get_job(payload["Task_id"]).state
            client.publish(
                "task_result", {"Task_id": payload["Task_id"], "state": state}
            )

    return handler


class GeneralPipeline:
    def __init__(self, scheduler: BackgroundScheduler, config: Dict):
        self.config = config
        self.serial = serial.Serial(port=config["port"], baudrate=config["baudrate"])
        self.sensors = self.extract_sensors(config)
        self.actuators = self.extract_actuators(config)
        self.mqtt_client = AdafruitConnector()
        self.scheduler = scheduler

    def setup_jobs(self):
        self.mqtt_client.addCallbackFn(mqtt_handler(self.scheduler))
        self.scheduler.add_job(
            read_sensors,
            "interval",
            args=[
                self.mqtt_client,
                config["device_feed"],
                self.sensors + self.actuators,
            ],
            seconds=0.5,
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
        return list_device

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
        return list_device

    def run(self, data):
        self.setup_jobs()
        self.scheduler.start()
        print("IOT Service is running ...")
        while True:
            pass
