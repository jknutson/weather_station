import time
from datetime import datetime
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import thread

class MQTTClient:
    def __init__(self, name, location, broker_ip, port) -> None:
        self.name = name
        self.location = location
        self.host = broker_ip
        self.port = port
        self.timeout = 60
        self.connected = 0
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.start()

    def start(self):
        self.client = mqtt.Client(self.name)
        self.client.connect(self.host, self.port, self.timeout)
        self.client.loop_start()

    def on_connect(self, userdata, flags, rc):
        if self.connected == 0:
            self.connected = 1
            print("Connected to MQTT, rc="+str(rc))
        self.client.subscribe(self.topic)

    def on_message(self, userdata, msg):
        message = str(msg.payload)
        print("MQTT "+msg.topic+': '+message)

    def on_publish(self, obj, mid):
        print("MQTT published "+str(mid))

    def publish(self, topic, payload):
        payload_str = json.dumps(
{'location': self.location, 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
  'payload': { payload }
})
        if self.connected == 0:
            self.start()
        mi = self.client.publish(topic, payload_str)
        rc = mi.rc
        if rc == MQTT_ERR_NO_CONN:
            self.connected = 0
        return rc

# client name'Weather station'
# host, port 192.168.0.105, 1883
# location 37.014835,-121.979731
# topic weather/data