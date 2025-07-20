import RPi.GPIO as GPIO

import logging
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)      # Use Broadcom pin numbering
GPIO.setwarnings(False)

class Motor:

  def __init__(self, name, pwm_pin, a_pin, b_pin):
    self.name = name
    
    logger.info(f"Motor {self.name} init start")
    
    self.pwm_pin = pwm_pin
    self.a_pin = a_pin
    self.b_pin = b_pin
    
    #Pin setup
    GPIO.setup(self.pwm_pin, GPIO.OUT)
    GPIO.setup(self.a_pin, GPIO.OUT) 
    GPIO.setup(self.b_pin, GPIO.OUT)
    
    #Initial pin setup
    GPIO.output(self.a_pin, GPIO.LOW) 
    GPIO.output(self.b_pin, GPIO.LOW)
    
    #PWM setup
    self.pwm = GPIO.PWM(self.pwm_pin, 1000)
    self.pwm.start(0)
    
    logger.info(f"Motor {self.name} initialized")
    
  def stop(self):
    logger.info(f"Motor {self.name} stop")
    
    #self.pwm.ChangeDutyCycle(0)
    GPIO.output(self.a_pin, GPIO.LOW) 
    GPIO.output(self.b_pin, GPIO.LOW)
  
  def forward(self):
    logger.info(f"Motor {self.name} forward")
    
    GPIO.output(self.a_pin, GPIO.HIGH) 
    GPIO.output(self.b_pin, GPIO.LOW)
  
  def reverse(self):
    logger.info(f"Motor {self.name} reverse")

    GPIO.output(self.a_pin, GPIO.LOW) 
    GPIO.output(self.b_pin, GPIO.HIGH)
    
  def set_speed(self, speed):
    logger.info(f"Motor {self.name} set speed {speed}")
    
    self.pwm.ChangeDutyCycle(speed)


