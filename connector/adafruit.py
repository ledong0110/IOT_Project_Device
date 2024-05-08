import sys
from Adafruit_IO import MQTTClient

class Adafruit_MQTT:
    AIO_FEED_IDs = ["button1", 	"button2"]
    AIO_USERNAME = "NPNLab_"
    AIO_KEY = "aio_"

    def connected(self, client):
        print("Connected ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)

    def subscribe(self, lient , userdata , mid , granted_qos):
        print("Subscribed...")
    
    def publish(self, feed_id, content):
        self.client.publish(feed_id, content)

    def disconnected(self, client):
        print("Disconnected...")
        sys.exit (1)

    def message(self, client , feed_id , payload):
        print("Received: '{}', Feed id: '{}'".format(payload, feed_id))
        if len(self.callback_fns):
            for fn in self.callback_fns:
               fn(feed_id, payload)

    def addCallbackFn(self, callback):
        self.callback_fns.append(callback)
        
    def __init__(self, username, key, feed_ids):
        self.AIO_USERNAME=username
        self.AIO_KEY=key
        self.AIO_FEED_IDS=feed_ids
        self.callback_fns = []
        self.client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
        self.client.on_connect = self.connected
        self.client.on_disconnect = self.disconnected
        self.client.on_message = self.message
        self.client.on_subscribe = self.subscribe
        self.client.connect()
        self.client.loop_background()
