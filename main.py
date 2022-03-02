# -*- coding:utf-8 -*-
import smbus
import RPi.GPIO as GPIO
from mlx90614 import MLX90614
import wiringpi

import time
from random import shuffle
import requests

#inside outside
angle = [
    (90,90),    #default
    (84,180),
    (77,175),
    (75,150),
    (55,205),
    (105,35),
    (100,15),
    (95,8),
    (125,-20)
]

# set motor offset if 90 degree not in middle
motor_offset = [-15,-15]

# setup thermo
temp1_address = 0x5a
thermo1 = MLX90614(temp1_address)

# setup servo motor
GPIO.setmode(GPIO.BCM)
servo_outer_pin = 12     # 外側
servo_inner_pin = 13     # 內側
servo_silk_pin = 6     # 微絲

# setup software pwm for silk motor
GPIO.setup(servo_silk_pin, GPIO.OUT)
motor_silk = GPIO.PWM(servo_silk_pin, 50) # PWM with 50Hz
motor_silk.start(1) # Initialization

# setup hardware pwm for normal motor
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

def move_motor_to_foot(i):
    move_motor_with_angle(servo_inner_pin,angle[i][0]+motor_offset[0])
    move_motor_with_angle(servo_outer_pin,angle[i][1]+motor_offset[1])

def move_motor_with_angle(motor,angle):
    wiringpi.pwmWrite(motor, int(100+angle/180*100))
    time.sleep(0.5)

def move_motor(motor,value):
    wiringpi.pwmWrite(value)
    time.sleep(0.5)

def get_random_order(start,end):
    # order = [1,2,3,4,5,6,7,8]
    order = list(range(start,end))
    shuffle(order)
    return order

def silk_out():
    motor_silk.ChangeDutyCycle(4.3+(120/180.0) * 5.0)

def silk_in():
    motor_silk.ChangeDutyCycle(4.3+(20/180.0) * 5.0)

def motor_init():
    move_motor_to_foot(0)
    silk_in()
    time.sleep(2)

def detect_temp():
    result = []
    for index in get_random_order(1,9):
        print('Running to foot',index)
        move_motor_to_foot(index)
        temp = get_temp(thermo1,temp1_address)
        print('Temp : ',temp)
        result.append(temp)
    return result


def post(datas, /, url=url):
    ''' function to post the test result to database

    datas: a list contain multiple test result, each as a dict.
           with structure like follow
           'memberid': int,
           'temp': int list with len == 10,
           'test': int list with len == 10
    '''

    for data in datas:
        data['temp'] = ', '.join([str(n) for n in data['temp']])
        data['test'] = ', '.join([str(n) for n in data['test']])
        print(data)
        r = requests.post(url, data=data)
        print(r.status_code)
        print(r.text)

if __name__ == '__main__':
    temp1 = get_temp(thermo1,temp1_address)
    print(temp1)

    print('System start!')
    #init
    motor_init()

    # running temp detect
    print(detect_temp())

    # running silk detect
    for index in get_random_order(1,9):
        print('Running to foot',index)
        move_motor_to_foot(index)
        silk_out()
        time.sleep(4)
        silk_in()
        time.sleep(0.5)
    


    