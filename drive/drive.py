import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

#import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    )
logger = logging.getLogger(__name__)


from framework.node import Node
from motor import Motor

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

#Node info
ROBOT_NAME = "myRobot"
NODE_NAME = "drive"
NODE_VERSION = "0.2"

CMD_TIMEOUT = 1 #in second

class drive(Node):
    STOPPED = "stopped"
    MOVING = "moving"
    
    def __init__(self):
        logger.info(f"{NODE_NAME} init start")
        
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
        
        logger.info(f"{NODE_NAME} inited")
    
    
    def _on_connect(self, client, userdata, flags, rc):
        logger.info(f"{NODE_NAME} on connect")
        
        self.publish_node_info()
        
        #Subscribe
        client.subscribe(self.move_service_topic)
        
    
    def _on_message(self, client, userdata, msg):
        
        topic_parts = msg.topic.split("/")
        payload = msg.payload.decode()
        
        logger.info(f"{NODE_NAME} message {msg.topic}: {payload}")
        
        #Move command
        if (msg.topic == self.move_service_topic):
            move_cmd = json.loads(payload)
            self.move(move_cmd)
            

    def move(self, move_cmd):
        logger.info(f"{NODE_NAME} message move")
        
        linear = move_cmd.get("linear", 0)
        angular = move_cmd.get("angular", 0)
            
        #Set Motor
        if (linear > 0 and angular == 0):
            self.motor_left.forward()
            self.motor_right.forward()
        elif (linear < 0 and angular == 0):
            self.motor_left.reverse()
            self.motor_right.reverse()
        elif (linear == 0 and angular > 0):
            print("positive angular")
            self.motor_left.forward()
            self.motor_right.reverse()
        elif (linear == 0 and angular < 0):
            print("negative angular")
            self.motor_left.reverse()
            self.motor_right.forward()
            
        self.last_cmd_time = time.time()
        self.publish_status(drive.MOVING)
    
    def publish_status(self, new_status):
    
        self.status = new_status
        self.publish(self.move_status_topic, self.status)
    
    def stop(self):
        logger.info(f"{NODE_NAME} stop")
        
        self.motor_left.stop()
        self.motor_right.stop()
        
        self.publish_status(drive.STOPPED)
    
    def set_speed(self, speed):
        self.motor_left.set_speed(speed)
        self.motor_right.set_speed(speed)
    
    def node_run(self):
        
        while True:
            #Check Command timeout
            if (self.status == drive.MOVING):
                if (time.time() - self.last_cmd_time) > CMD_TIMEOUT:
                    self.stop()
            
            time.sleep(0.01)

#Main entry point
if __name__ == "__main__":
    try:
        myDrive = drive()
        
        myDrive.node_run()
            
    except KeyboardInterrupt:
        logger.error(f"{NODE_NAME} Interrupted by user, exiting gracefully.")
        
    except Exception as e:
        logger.error(f"{NODE_NAME} An error occurred: {e}")
            
    finally:
        logger.error(f"{NODE_NAME} Finally")
