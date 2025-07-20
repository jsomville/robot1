import paho.mqtt.client as mqtt

class Node:
    
    def __init__(self, robot_name, name, version):
        print("node init")
        self.robot_name = robot_name
        self.node_name = name
        self.version = version
        
        self.services = None
        
        self.main_topic = f"{self.robot_name}/node/{self.node_name}"
        self.node_status_topic = f"{self.main_topic}/node_status"
        
        #Last will topic
        self.last_will_topic = self.node_status_topic
        self.last_will_value = "Disconnected"
        
        #Mqtt Client
        self.client = mqtt.Client()
        
        print(f"node initialized")
        
    
    def connect(self, broker, port, keep_alive):
        print(f"node connect")
        
        #set last will
        self.client.will_set(self.last_will_topic, payload=self.last_will_value, qos=1)
        
        self.client.connect(broker, port, keep_alive)
        self.client.loop_start()
    
    def publish_node_info(self):
        
        topic = f"{self.main_topic}/version"
        self.publish(topic, self.version)
        
        self.publish(self.node_status_topic, "Connected")
        
        if (self.services != None):
            topic = f"{self.main_topic}/services"
            self.publish(topic, self.services)
        
    
    def publish(self, topic, value):
        self.client.publish(topic, value)
    
    def subscribe(self, topic):
        self.client.subscribe(topic)
        
        