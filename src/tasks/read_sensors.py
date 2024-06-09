from typing import List
from ..device_wrapper import RS485
from ..connector import AdafruitConnector
import json
from ..config import glob_var


def read_sensors(feed_id: str, sensors: List[RS485]):
    data = json.dumps({sensor.get_name(): sensor.read() for sensor in sensors})
    glob_var.mqtt_client.publish(feed_id=feed_id, content=data)
