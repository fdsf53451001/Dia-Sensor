# -*- coding:utf-8 -*-
import smbus
import RPi.GPIO as GPIO
from mlx90614 import MLX90614

import time

# setup thermo
temp1_address = 0x5a
thermo1 = MLX90614(temp1_address)

# setup servo motor
servo1_pin = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1_pin, GPIO.OUT)
motor1 = GPIO.PWM(servo1_pin, 50) # GPIO 17 for PWM with 50Hz
motor1.start(2.5) # Initialization

def get_temp(thermo,address):
    try:
        return thermo.get_obj_temp()
    except IOError as e:
        print('temp sensor error!')
        return -1

def move_motor(motor,angle):
    motor.ChangeDutyCycle(5)
    time.sleep(0.5)


if __name__ == '__main__':

    temp1 = get_temp(thermo1,temp1_address)
    print(temp1)

    move_motor(motor1,5)
    move_motor(motor1,10)
    move_motor(motor1,5)


    