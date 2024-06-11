import time
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.events import EVENT_JOB_ERROR
import serial
import serial.tools.list_ports
from src.device_wrapper import Relay, Sensor
from dotenv import load_dotenv
import json

load_dotenv()
from src.config import glob_var
from src.pipelines import GeneralPipeline

jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///database/jobs.sqlite")}
executors = {"default": ThreadPoolExecutor(10), "processpool": ProcessPoolExecutor(3)}
job_defaults = {"coalesce": False, "max_instances": 2}
scheduler = BackgroundScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone="Asia/Ho_Chi_Minh",
)


def listener(event):
    glob_var.mqtt_client.publish("task_result", json.dumps({"Task_id": event.job_id, "state": 0}))


scheduler.add_listener(listener, EVENT_JOB_ERROR)

with open("system_config.json") as f:
    system_config = json.load(f)

portName = system_config["port"]
baundrate = system_config["baudrate"]

try:
    ser = serial.Serial(port=portName, baudrate=baundrate)
    print("Open successfully")
except:
    print("Can not open the port")

pipeline = GeneralPipeline(ser, scheduler, system_config)
pipeline.run()
