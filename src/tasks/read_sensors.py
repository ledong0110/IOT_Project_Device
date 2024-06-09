from typing import List
from ..device_wrapper import Relay, Sensor
from ..connector import AdafruitConnector
import json
from ..config import glob_var


def read_sensors(feed_id: str):
    data = json.dumps({sensor.get_name(): sensor.read() if type(sensor) is Sensor else sensor.get_state() for sensor in glob_var.list_sensors+glob_var.list_actuators})
    glob_var.mqtt_client.publish(feed_id=feed_id, content=data)
