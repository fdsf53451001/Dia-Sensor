# -*- coding:utf-8 -*-
import smbus
import RPi.GPIO as GPIO
from mlx90614 import MLX90614
import wiringpi

import time
from random import shuffle

#inside outside
angle = [
    (84,185),
    (80,170),
    (75,150),
    (57,205),
    (84,185),
    (80,170),
    (75,150),
    (57,205)
]

# setup thermo
temp1_address = 0x5a
thermo1 = MLX90614(temp1_address)

# setup servo motor
GPIO.setmode(GPIO.BCM)
servo_outer_pin = 12     # 外側
servo_inner_pin = 13     # 內側
servo_silk_pin = 18     # 微絲

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(servo_outer_pin, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servo_inner_pin, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servo_silk_pin, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

def get_temp(thermo,address):
    try:
        return thermo.get_obj_temp()
    except IOError as e:
        print('temp sensor error!')
        return -1

def move_motor_with_angle(motor,angle):
    wiringpi.pwmWrite(motor, int(100+angle/180*100))
    time.sleep(0.5)

def move_motor(motor,value):
    wiringpi.pwmWrite(value)
    time.sleep(0.5)

def set_silk(status):
    if not status:
        move_motor_with_angle(servo_silk_pin,70)
    else:
        move_motor_with_angle(servo_silk_pin,90)

def get_random_order():
    order = [0,1,2,3,4,5,6,7]
    shuffle(order)
    return order

if __name__ == '__main__':
    temp1 = get_temp(thermo1,temp1_address)
    print(temp1)

    servo_outer_offset = -15
    servo_inner_offset = -15
    print('Input offset (inner,outter):')
    servo_inner_offset = int(input())
    servo_outer_offset = int(input())

    while True:
        #init
        move_motor_with_angle(servo_outer_pin,90+servo_outer_offset)
        move_motor_with_angle(servo_inner_pin,90+servo_inner_offset)
        time.sleep(2)

        for index in get_random_order():
            move_motor_with_angle(servo_outer_pin,angle[index][1]+servo_outer_offset)
            move_motor_with_angle(servo_inner_pin,angle[index][0]+servo_inner_offset)
            set_silk(1)
            time.sleep(2)
            set_silk(0)

        # move_motor_with_angle(motor1,135)
        # move_motor_with_angle(motor2,81)
        # time.sleep(2)

        # move_motor(motor2,7)
        # time.sleep(1)
        # move_motor(motor2,7.5)
        # time.sleep(1)



    