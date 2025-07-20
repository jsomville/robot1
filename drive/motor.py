import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)      # Use Broadcom pin numbering
GPIO.setwarnings(False)

class Motor:

  def __init__(self, name, pwm_pin, a_pin, b_pin):
    print("motor init")
    
    self.name = name
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
    
    print(f"motor {self.name} initialized")
    
  def stop(self):
    print(f"motor {self.name} stop")
    #self.pwm.ChangeDutyCycle(0)
    GPIO.output(self.a_pin, GPIO.LOW) 
    GPIO.output(self.b_pin, GPIO.LOW)
  
  def forward(self):
    print(f"motor {self.name} forward") 
    GPIO.output(self.a_pin, GPIO.HIGH) 
    GPIO.output(self.b_pin, GPIO.LOW)
  
  def reverse(self):
    print(f"motor {self.name} reverse")
    GPIO.output(self.a_pin, GPIO.LOW) 
    GPIO.output(self.b_pin, GPIO.HIGH)
    
  def set_speed(self, speed):
    self.pwm.ChangeDutyCycle(speed)


