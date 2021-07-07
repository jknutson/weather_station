import sys
sys.path.append('..')
import MQTT
import time

client = MQTT.MQTTClient('test', 'test location', 'test/topic', '192.168.0.105', 1883)
dummy_payload = {'dummy': {'value1': 1, 'value2': 'apple', 'value3': (1,2,3)}}
client.publish('test/topic', dummy_payload)
time.sleep(10)
