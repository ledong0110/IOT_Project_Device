from ..connector import AdafruitConnector

mqtt_client = AdafruitConnector(feed_ids=["task-action", "task-result-query"])
list_sensors = []
list_actuators = []
