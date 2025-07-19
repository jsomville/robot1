import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json


#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

#Node info
robot_name = "myRobot"
node_name = "drive"
version = "0.1"

#Topic info
main_topic = f"{robot_name}/node/{node_name}"
node_status_topic = f"{main_topic}/status"
move_service_topic = f"{robot_name}/service/move"
move_status_topic = f"{robot_name}/service/move/status"

#Move service Status
STOPPED = "stopped"
MOVING = "moving"
status = STOPPED
last_cmd_time = time.time()
CMD_TIMEOUT = 2 #in second

def publish_node_info():
    now = datetime.now()
    client.publish(main_topic, now.isoformat())
    
    topic = f"{main_topic}/version"
    client.publish(topic, version)
    
    client.publish(node_status_topic, "Connected")
    
    topic = f"{main_topic}/services"
    client.publish(node_status_topic, "move")
    
    #Subscription
    client.subscribe(move_service_topic)


def on_connect(client, userdata, flags, rc):
    print(f"Node {node_name} connected")
    
    publish_node_info()
    

def on_message(client, userdata, msg):
    global last_cmd_time
    
    topic_parts = msg.topic.split("/")
    payload = msg.payload.decode()
     
    print(f"Node {node_name} recieved {msg.topic}: {payload}")
    
    #Move command
    if (msg.topic == move_service_topic):
        print(f"Drive - Moving ")
        
        move_cmd = json.loads(payload)
        linear = move_cmd.get("linear", 0)
        angular = move_cmd.get("angular", 0)
        
        last_cmd_time = time.time()
        publish_status(MOVING)


def stop():
    print(f"Drive - Stopped ")
    publish_status(STOPPED)

def publish_status(new_status):
    global status
    
    status = new_status
    client.publish(move_status_topic, status)
           

def check_timeout():
    global status
    
    if (status == MOVING):
        if (time.time() - last_cmd_time) > CMD_TIMEOUT:
            stop()
    
    
#Connect to Broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.will_set(node_status_topic, payload="Disconnected", qos=1, retain=True)
client.connect(broker, port, keep_alive)
client.loop_start()

try:
    while True:
        check_timeout()
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("Interrupted by user, exiting gracefully.")
    
except Exception as e:
    print(f"An error occurred: {e}")
        
finally:
    print('Finally')
