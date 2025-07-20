import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

from node import Node

from motor import Motor

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

#Node info
ROBOT_NAME = "myRobot"
NODE_NAME = "drive"
NODE_VERSION = "0.1"

CMD_TIMEOUT = 1 #in second

class drive(Node):
    STOPPED = "stopped"
    MOVING = "moving"
    
    def __init__(self):
        print("drive init")
        
        self.last_cmd_time = time.time()
        self.status = drive.STOPPED
        
        super().__init__(ROBOT_NAME, NODE_NAME, NODE_VERSION)
        
        self.services = "None"
        self.move_service_topic = f"{ROBOT_NAME}/service/move"
        self.move_status_topic = f"{ROBOT_NAME}/service/move/status"
        
        #Create Motor
        self.motor_left = Motor("left", 13, 6, 5)
        self.motor_right = Motor("right", 12, 25, 26)
        self.set_speed(60)
        
        #MQTT connect
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
        self.connect(broker, port, keep_alive)
    
    
    def _on_connect(self, client, userdata, flags, rc):
        print(f"{NODE_NAME} on connect")
        
        self.publish_node_info()
        
        #Subscribe
        client.subscribe(self.move_service_topic)
        
    
    def _on_message(self, client, userdata, msg):
        
        topic_parts = msg.topic.split("/")
        payload = msg.payload.decode()
        
        print(f"Node {NODE_NAME} recieved {msg.topic}: {payload}")
        
        #Move command
        if (msg.topic == self.move_service_topic):
            print(f"Drive - Moving ")
            
            move_cmd = json.loads(payload)
            self.move(move_cmd)
            

    def move(self, move_cmd):
        linear = move_cmd.get("linear", 0)
        angular = move_cmd.get("angular", 0)
            
        #Set Motor
        if linear > 0:
            self.motor_left.forward()
            self.motor_right.forward()
        elif linear < 0:
            self.motor_left.reverse()
            self.motor_right.reverse()
            
        self.last_cmd_time = time.time()
        self.publish_status(drive.MOVING)
    
    def publish_status(self, new_status):
    
        self.status = new_status
        self.publish(self.move_status_topic, self.status)
    
    def stop(self):
        print(f"Drive - Stopped ")
        
        self.motor_left.stop()
        self.motor_right.stop()
        
        self.publish_status(drive.STOPPED)
    
    def set_speed(self, speed):
        self.motor_left.set_speed(speed)
        self.motor_right.set_speed(speed)
    
    def node_run(self):
        #Check Command timeout
        if (self.status == drive.MOVING):
            if (time.time() - self.last_cmd_time) > CMD_TIMEOUT:
                self.stop()

try:
    myDrive = drive()
    
    while True:
        myDrive.node_run()
        
        time.sleep(0.01)
        
except KeyboardInterrupt:
    print("Interrupted by user, exiting gracefully.")
    
except Exception as e:
    print(f"An error occurred: {e}")
        
finally:
    print('Finally')
