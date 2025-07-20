import paho.mqtt.client as mqtt
from datetime import datetime

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

#Topic
topic = "#"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    
    #Subscribe
    client.subscribe(topic)

def on_message(client, userdata, msg):
    topic_parts = msg.topic.split("/")
    payload = msg.payload.decode()
     
    now = datetime.now()
    now.isoformat()
     
    print(f"{now.isoformat()} {msg.topic} : {payload}")

try:

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Subscriber started")

    client.connect(broker, port, keep_alive)
    
    client.loop_forever()
    
except KeyboardInterrupt:
    print("Subscriber interrupted by user, exiting gracefully.")
    
except Exception as e:
    print(f"Subscriber - An error occurred: {e}")
        
finally:
    print('Subscriber - Finally')