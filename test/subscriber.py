import paho.mqtt.client as mqtt

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60


#Topic
robot_name = "myRobot"
example_topic = "say"
topic = f"{robot_name}/{example_topic}"
topic = "#"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    
    #Subscribe
    client.subscribe(topic)

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    payload = msg.payload.decode()
     
    print(f"Received on topic {msg.topic}: {payload}")



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, port, keep_alive)
client.loop_forever()
