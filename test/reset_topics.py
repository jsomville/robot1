import paho.mqtt.client as mqtt
from datetime import datetime

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

client = mqtt.Client()

client.connect(broker, port, keep_alive)

client.publish("myRobot/node/drive/status", "")

client.publish("myRobot/node/drive/node_status", "")