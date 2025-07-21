import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
import json

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    )
logger = logging.getLogger(__name__)

from evdev import InputDevice, categorize, ecodes, list_devices

from framework.node import Node

#Node info
ROBOT_NAME = "myRobot"
NODE_NAME = "remote"
NODE_VERSION = "0.1"

#Broker Connexions
broker = "localhost"  # or IP address of your broker
port = 1883
keep_alive = 60

keyboard_id=""

class remote(Node):
    
    def __init__(self):
        logger.info(f"{NODE_NAME} init start")
        
        super().__init__(ROBOT_NAME, NODE_NAME, NODE_VERSION)
        
        self.move_topic = f"{ROBOT_NAME}/service/move"
        
        self.connect(broker, port, keep_alive)
        
        logger.info(f"{NODE_NAME} inited")
        
        #self.find_keyboard_device()
        
    def _on_connect(self, client, userdata, flags, rc):
        logger.info(f"{NODE_NAME} on connect")
        
        self.publish_node_info()
    
    def on_keypressed(self, keycode):
        
        match keycode:
            case "KEY_U":
                self.move_command(1, 0)
            case "KEY_D":
                self.move_command(-1, 0)
            case "KEY_L":
                self.move_command(0, -1)
            case "KEY_R":
                self.move_command(0, 1)
            case "KEY_UP":
                self.move_command(1, 0)
            case "KEY_DOWN":
                self.move_command(-1, 0)
            case "KEY_LEFT":
                self.move_command(0, -1)
            case "KEY_RIGHT":
                self.move_command(0, 1)
    
    def move_command(self, linear, angular):
        
        move_cmd = {
            "linear": linear,
            "angular": angular
        }
        
        self.publish(self.move_topic,  json.dumps(move_cmd))
    
    def find_keyboard_device(self):
        devices = [InputDevice(path) for path in list_devices()]
        
        for device in devices:
            print(f"{device.name} {device.path}")
            if 'mouse' in device.name.lower():
                print(device.path)
                return device.path
        return None
            
    def node_run(self):
        
        while True:
            
            dev = InputDevice('/dev/input/event0')
            for event in dev.read_loop():
                if event.type == ecodes.EV_KEY:
                    key_event = categorize(event)
                    if key_event.keystate == key_event.key_down:
                        print(f"Key pressed: {key_event.keycode} on event4")

                        self.on_keypressed(key_event.keycode)
            time.sleep(0.01)
    
    

#Main entry point
if __name__ == "__main__":
    try:
        myRemote = remote()
        
        myRemote.node_run()
            
    except KeyboardInterrupt:
        print("Interrupted by user, exiting gracefully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
            
    finally:
        print('Finally')


