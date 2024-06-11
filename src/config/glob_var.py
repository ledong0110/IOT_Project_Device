from ..connector import AdafruitConnector

mqtt_client = AdafruitConnector(feed_ids=["ledong0110/feeds/task-action", "ledong0110/feeds/task-result-query"])
list_sensors = []
list_actuators = []
