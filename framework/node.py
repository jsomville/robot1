import paho.mqtt.client as mqtt
import time
import json

import logging
logger = logging.getLogger(__name__)

class Node:
    
    def __init__(self, robot_name, name, version):
        
        logger.info(f"Node init start")
        
        self.robot_name = robot_name
        self.node_name = name
        self.version = version
        
        self.services = None
        self.parameters_updated = False
        
        self.main_topic = f"{self.robot_name}/node/{self.node_name}"
        self.node_status_topic = f"{self.main_topic}/node_status"
        self.parameters_topic = f"{self.main_topic}/parameters"
        
        #Last will topic
        self.last_will_topic = self.node_status_topic
        self.last_will_value = "Disconnected"
        
        #Mqtt Client
        self.client = mqtt.Client()
        
        logger.info(f"Node initialized")
        
    
    def connect(self, broker, port, keep_alive):
        logger.info(f"Node connect")
        
        #set last will
        self.client.will_set(self.last_will_topic, payload=self.last_will_value, qos=1)
        
        self.client.connect(broker, port, keep_alive)
        self.client.loop_start()
        
        self.broker_connected_time = time.time()
    
    def publish_node_info(self):
        logger.info(f"Node publish node info")
        
        topic = f"{self.main_topic}/version"
        self.publish(topic, self.version)
        
        self.publish(self.node_status_topic, "Connected")
        
        if (self.services != None):
            topic = f"{self.main_topic}/services"
            self.publish(topic, self.services)
        
    
    def publish(self, topic, value):
        self.client.publish(topic, value)
    
    def publish_retained(self, topic, value):
        self.client.publish(topic, value, retain=True)
    
    def subscribe(self, topic):
        self.client.subscribe(topic)
        
    def update_parameters(self):
        logger.info(f"Node update parameters {self.parameters}")
        
        self.publish_retained(self.parameters_topic, json.dumps(self.parameters))
    
    def tick(self):
        
        #Update parameters if messaged not retained
        if (time.time() - self.broker_connected_time) > 1:
            if not self.parameters_updated :
                self.update_parameters()
        
        
        