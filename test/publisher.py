import paho.mqtt.client as mqtt

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60


#Connect to Broker
client = mqtt.Client()
client.connect(broker, port, keep_alive)


#Topic
robot_name = "myRobot"
example_topic = "say"
topic = f"{robot_name}/{example_topic}"


# Publish a message
value = "Hello !!"
client.publish(topic, value)
print(f"Published {value} to topic '{topic}'")

client.disconnect()
