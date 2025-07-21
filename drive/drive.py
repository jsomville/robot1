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

#This default parameters
MIN_SPEED = 50
MAX_SPEED = 100
CMD_TIMEOUT = 1 #in second
CYCLE = 60 #in HZ

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
        
        #Parameters
        self.init_parameters()
        
        #Create Motor
        self.motor_left = Motor("left", 13, 6, 5)
        self.motor_right = Motor("right", 12, 25, 26)
        min_speed = self.parameters.get("min_speed", MIN_SPEED)
        self.set_speed(min_speed)
        
        #MQTT connect
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
        self.connect(broker, port, keep_alive)
        
        logger.info(f"{NODE_NAME} inited")
    
    def init_parameters(self):
        
        parameters = {
            "min_speed": MIN_SPEED,
            "max_speed": MAX_SPEED,
            "cmd_timeout" : CMD_TIMEOUT,
            "cycle" : CYCLE
        }
        
        self.cycle_time = 1 / CYCLE
        self.parameters = parameters
    
    def _on_connect(self, client, userdata, flags, rc):
        logger.info(f"{NODE_NAME} on connect")
        
        self.publish_node_info()
        
        #Subscribe
        client.subscribe(self.move_service_topic)
        client.subscribe(self.parameters_topic)
        
    
    def _on_message(self, client, userdata, msg):
        
        topic_parts = msg.topic.split("/")
        payload = msg.payload.decode()
        
        logger.info(f"{NODE_NAME} message {msg.topic}: {payload}")
        
        match msg.topic :
            case self.move_service_topic:
                move_cmd = json.loads(payload)
                self.move(move_cmd)
            case self.parameters_topic:
                parameters = json.loads(payload)
                self.parse_parameters(parameters)
                    
                    
    def parse_parameters(self, parameters):
        logger.info(f"{NODE_NAME} parse new parameters {parameters}")
        self.parameters_updated = True
    
        try:
            val = parameters.get("min_speed", MIN_SPEED)
            if self.parameters["min_speed"] != val :
                self.parameters["min_speed"] = val
            val = parameters.get("max_speed", MAX_SPEED)   
            if self.parameters["max_speed"] != val :
                self.parameters["max_speed"] = val
            val = parameters.get("cmd_timeout", CMD_TIMEOUT)
            if self.parameters["cmd_timeout"]!= val :
                self.parameters["cmd_timeout"] = val
            val = parameters.get("cycle", CYCLE)
            if self.parameters["cycle"]!= val :
                self.parameters["cycle"] = val
                self.cycle_time = 1 / val
        except Exception as e:
            logger.error(f"{NODE_NAME} update parameters : {e}")
            

    def move(self, move_cmd):
        logger.info(f"{NODE_NAME} message move")
        
        linear = move_cmd.get("linear", 0)
        angular = move_cmd.get("angular", 0)
        
        #check if was previously moving and adjust speed
        if (self.status == drive.STOPPED):
            min_speed = self.parameters.get("min_speed", MIN_SPEED)
            self.set_speed(min_speed)
        else:
            max_speed = self.parameters.get("max_speed", MAX_SPEED)
            self.set_speed(max_speed)
        
        #Set Motor
        if (linear > 0 and angular == 0):
            self.motor_left.forward()
            self.motor_right.forward()
            self.publish_status(drive.MOVING)
        elif (linear < 0 and angular == 0):
            self.motor_left.reverse()
            self.motor_right.reverse()
            self.publish_status(drive.MOVING)
        elif (linear == 0 and angular > 0):
            self.motor_left.reverse()
            self.motor_right.forward()
            self.publish_status(drive.MOVING)
        elif (linear == 0 and angular < 0):
            self.motor_left.forward()
            self.motor_right.reverse()
            self.publish_status(drive.MOVING)
        elif (linear == 0 and angular == 0):
            self.stop()
            
        self.last_cmd_time = time.time()
        
    
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
            self.tick()
            
            #Check Command timeout
            if (self.status == drive.MOVING):
                if (time.time() - self.last_cmd_time) > CMD_TIMEOUT:
                    self.stop()
            
            time.sleep(self.cycle_time)

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
