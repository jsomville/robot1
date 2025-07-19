import RPi.GPIO as GPIO
import time

MOTORA_PWM = 13
MOTORA_A = 6
MOTORA_B = 5

MOTORB_PWM = 12
MOTORB_A = 25
MOTORB_B = 26

GPIO.setmode(GPIO.BCM)      # Use Broadcom pin numbering
#Motor A
GPIO.setup(MOTORA_PWM, GPIO.OUT)
GPIO.setup(MOTORA_A, GPIO.OUT) 
GPIO.setup(MOTORA_B, GPIO.OUT)
pwm_a = GPIO.PWM(MOTORA_PWM, 1000)
pwm_a.start(0)

#Motor B
GPIO.setup(MOTORB_PWM, GPIO.OUT)
GPIO.setup(MOTORB_A, GPIO.OUT) 
GPIO.setup(MOTORB_B, GPIO.OUT)
pwm_b = GPIO.PWM(MOTORB_PWM, 1000)
pwm_b.start(0)


def motor_a_on():
	print("motor A on")
	#GPIO.output(MOTORA_PWM, GPIO.HIGH)
	GPIO.output(MOTORA_A, GPIO.LOW) 
	GPIO.output(MOTORA_B, GPIO.LOW) 


def motor_a_off():
  print("motor A off")
  #GPIO.output(MOTORA_PWM, GPIO.LOW)
  pwm_a.ChangeDutyCycle(0)
  GPIO.output(MOTORA_A, GPIO.LOW)
  GPIO.output(MOTORA_B, GPIO.LOW)

def motor_a_fwd():
  print("motor A fwd")
  GPIO.output(MOTORA_A, GPIO.HIGH)
  GPIO.output(MOTORA_B, GPIO.LOW)

def motor_a_rev():
  print("motor A rev")
  GPIO.output(MOTORA_A, GPIO.LOW)
  GPIO.output(MOTORA_B, GPIO.HIGH)
  
def motor_b_on():
  print("motor B on")
  #GPIO.output(MOTORB_PWM, GPIO.HIGH)
  pwm_b.ChangeDutyCycle(0)
  GPIO.output(MOTORB_A, GPIO.LOW) 
  GPIO.output(MOTORB_B, GPIO.LOW) 

def motor_b_off():
  print("motor B off")
  #GPIO.output(MOTORB_PWM, GPIO.LOW)
  pwm_b.ChangeDutyCycle(0)
  GPIO.output(MOTORB_A, GPIO.LOW)
  GPIO.output(MOTORB_B, GPIO.LOW)

def motor_b_fwd():
  print("motor B fwd")
  GPIO.output(MOTORB_A, GPIO.HIGH)
  GPIO.output(MOTORB_B, GPIO.LOW)

def motor_b_rev():
  print("motor B rev")
  GPIO.output(MOTORB_A, GPIO.LOW)
  GPIO.output(MOTORB_B, GPIO.HIGH)

def set_motor_speeds(speed):
  print(f"set speed {speed}")
  pwm_a.ChangeDutyCycle(speed)
  pwm_b.ChangeDutyCycle(speed)

try:
  motor_a_on()
  motor_b_on()
  time.sleep(1)
  
  while True:
      print("FWD sequence")
      motor_a_fwd()
      motor_b_fwd()
      
      #Increase Speed
      for speed in range(0, 101, 10):
        set_motor_speeds(speed)
        time.sleep(2)
      
      
      print("REV sequence")
      motor_a_rev()
      motor_b_rev()
      
      #Increase Speed
      for speed in range(0, 101, 10):
        set_motor_speeds(speed)
        time.sleep(2)
    
  
  print("Off Motors")
  motor_a_off()
  motor_b_off()

except KeyboardInterrupt:
  GPIO.cleanup()                 # Reset all GPIOs


