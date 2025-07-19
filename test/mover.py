import paho.mqtt.client as mqtt
import json

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60


#Connect to Broker
client = mqtt.Client()
client.connect(broker, port, keep_alive)


#Topic
robot_name = "myRobot"
topic = f"{robot_name}/service/move"


# Publish a move command

move_cmd = {
    "linear": 0.3,
    "angular": 0.1
}

client.publish(topic, json.dumps(move_cmd))

client.disconnect()
