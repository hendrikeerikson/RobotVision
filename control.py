import RPi.GPIO as GPIO
from constants import *

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(7, GPIO.OUT)  # PWMA
GPIO.setup(11, GPIO.OUT)  # AIN2
GPIO.setup(12, GPIO.OUT)  # AIN1
GPIO.setup(13, GPIO.OUT)  # STBY
GPIO.setup(15, GPIO.OUT)  # BIN1
GPIO.setup(16, GPIO.OUT)  # BIN2
GPIO.setup(18, GPIO.OUT)  # PWMB

# Clockwise AIN1/BIN1 = HIGH and AIN2/BIN2 = LOW
# Counter-Clockwise: AIN1/BIN1 = LOW and AIN2/BIN2 = HIGH

pwma = GPIO.PWM(7, 50)
pwmb = GPIO.PWM(18, 50)

GPIO.output(12, GPIO.HIGH)  # Set AIN1
GPIO.output(11, GPIO.LOW)  # Set AIN2

GPIO.output(15, GPIO.HIGH)  # Set BIN1
GPIO.output(16, GPIO.LOW)  # Set BIN2

pwma.start(0)
pwmb.start(0)

GPIO.output(13, GPIO.HIGH)


def motor_speeds(point):
    x = point[0]
    # set origin in the middle of the screen
    x -= WIDTH//2

    if abs(x) < FMW:
        return 1, 1

    elif x > 0:
        return 1, ROT

    elif x < 0:
        return ROT, 1


def set_motors(speeds):
    max_speed = 40

    pwmb.ChangeDutyCycle(max_speed * speeds[0])
    pwma.ChangeDutyCycle(max_speed * speeds[1])


def cleanup():
    pwma.stop()
    pwmb.stop()

    GPIO.cleanup()
