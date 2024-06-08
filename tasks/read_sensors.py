from typing import List, String
from device_wrapper import RS485
from connector import AdafruitConnector


def read_sensors(mqtt_client: AdafruitConnector, feed_id: String, sensors: List[RS485]):
    data = {sensor.get_name(): sensor.read() for sensor in sensors}
    mqtt_client.publish(feed_id=feed_id, content=data)
