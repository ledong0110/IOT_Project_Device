import sys
from typing import List
from Adafruit_IO import MQTTClient
import os


class AdafruitConnector:
    AIO_FEED_IDs: List
    AIO_USERNAME: str
    AIO_KEY: str

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(f"{feed}")

    def add_feed_id(self, feed_id):
        self.AIO_FEED_IDs.append(feed_id)
        self.client.subscribe(f"{feed}")

    def subscribe(self, client, userdata, mid, granted_qos):
        print("Subscribed...")

    def publish(self, feed_id, content):
        self.client.publish(feed_id, content)

    def disconnected(self, client):
        print("Disconnected...")
        raise SystemError("Disconnected from Adafruit IO")

    def message(self, client, feed_id, payload):
        print("Received: '{}', Feed id: '{}'".format(payload, feed_id))
        if len(self.callback_fns):
            for fn in self.callback_fns:
                fn(feed_id, payload)

    def addCallbackFn(self, callback):
        self.callback_fns.append(callback)

    def __init__(
        self,
        username=os.getenv("Adafruit_Username"),
        key=os.getenv("Adafruit_Key"),
        feed_ids=[],
    ):
        self.AIO_USERNAME = username
        self.AIO_KEY = key
        self.AIO_FEED_IDs = feed_ids
        self.callback_fns = []
        self.client = MQTTClient(self.AIO_USERNAME, self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()
