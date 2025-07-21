import paho.mqtt.client as mqtt
from datetime import datetime
import json

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

client = mqtt.Client()

client.connect(broker, port, keep_alive)

parameters = {
    "min_speed": 60,
    "max_speed": 100,
    "cmd_timeout" : 1,
    "cycle" : 62
}

client.publish("myRobot/node/drive/parameters", json.dumps(parameters), retain=True)
