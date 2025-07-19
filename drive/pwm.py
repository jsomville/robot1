import RPi.GPIO as GPIO
import time

pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

pwm = GPIO.PWM(pin, 1000)
pwm.start(0)

try:
    while True:
        for duty in range(0, 101, 5):
            print(f"Duty: {duty}%")
            pwm.ChangeDutyCycle(duty)
            time.sleep(0.1)
except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
