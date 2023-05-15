from threading import Thread
import paho.mqtt.client as mqtt
from time import sleep as delay
from collections import deque
from datetime import datetime as dt

class MqttClient(Thread):

    def __init__(self, serverUrl, port, topic):
        super().__init__()
        self.mqttc = mqtt.Client()
        self.server = serverUrl
        self.port = port
        self.topic = topic
        self.queue = deque()


    def run(self):
        self.mqttc.on_connect = self.onConnect
        self.mqttc.on_disconnect = self.onDisconnect
        self.mqttc.on_subscribe = self.onSubscribe
        self.mqttc.on_message = self.onMessage
        self.mqttc.connect(host=self.server, port=self.port)
        self.mqttc.loop_forever()

    def onConnect(self, mqttc, userdata, flags, rc):
        print("Uspjesno spojeni na server!")
        self.mqttc.subscribe(topic=self.topic, qos=0)

    def onDisconnect(self, mqttc, userdata, rc):
        print("Disconnected...")

    def onSubscribe(self, mqttc, userdata, mid, granted_qos):
        print("Uspjesno pretplaceni sa qos: " + str(granted_qos))

    def onMessage(self, mqttc, userdata, msg):
        #print(msg.topic + " - " + msg.payload.decode("utf-8"))
        self.queue.append(f"{msg.topic};{msg.payload.decode('utf-8')};{str(dt.now().timestamp())}")

    def publish(self, msg, topic):
        #print(f"Publishing... topic[{topic}]: {msg}")
        self.mqttc.publish(topic, msg, 0, False)

    def getFromQueue(self):
        if len(self.queue) != 0:
            return self.queue.popleft()
        else:
            return None
