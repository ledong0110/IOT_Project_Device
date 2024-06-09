from typing import List
from ..device_wrapper import RS485
from ..connector import AdafruitConnector
import json
from ..config import glob_var


def read_sensors(feed_id: str):
    data = json.dumps({sensor.get_name(): sensor.read() for sensor in glob_var.sensors+glob_var.actuators})
    glob_var.mqtt_client.publish(feed_id=feed_id, content=data)
