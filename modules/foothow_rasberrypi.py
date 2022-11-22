# -*- coding:utf-8 -*-
import smbus
import RPi.GPIO as GPIO
from mlx90614 import MLX90614
import wiringpi

import time
from random import shuffle
import requests

class Foothow_Rasberrypi:

    def __init__(self) -> None:
        
        #inside outside
        self.angle = [
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

        self.silk_start = 1
        self.silk_end = 9

        # set motor offset if 90 degree not in middle
        self.motor_offset = [-15,-15]

        # setup thermo
        self.temp1_address = 0x5a
        self.thermo1 = MLX90614(self.temp1_address)

        # setup servo motor
        GPIO.setmode(GPIO.BCM)
        self.servo_outer_pin = 12     # 外側
        self.servo_inner_pin = 13     # 內側
        self.servo_silk_pin = 6     # 微絲

        # setup software pwm for silk motor
        GPIO.setup(self.servo_silk_pin, GPIO.OUT)
        self.motor_silk = GPIO.PWM(self.servo_silk_pin, 50) # PWM with 50Hz
        self.motor_silk.start(1) # Initialization

        # setup random move path
        self.foot_move_array = []
        self.set_random_order()
        self.current_arm_index = 0

        # setup hardware pwm for normal motor
        # use 'GPIO naming'
        wiringpi.wiringPiSetupGpio()

        # set #18 to be a PWM output
        wiringpi.pinMode(self.servo_outer_pin, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pinMode(self.servo_inner_pin, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pinMode(self.servo_silk_pin, wiringpi.GPIO.PWM_OUTPUT)

        # set the PWM mode to milliseconds stype
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

    def get_temp(self,thermo,address):
        try:
            return thermo.get_obj_temp()
        except IOError as e:
            print('temp sensor error!')
            return -1

    def move_motor_to_next(self):
        if self.foot_move_array == []:
            return -1
        self.current_arm_index = self.foot_move_array.pop(0)
        self.move_motor_to_foot(self.current_arm_index)
        return self.current_arm_index

    def move_motor_to_foot(self,i):
        self.move_motor_with_angle(self.servo_inner_pin,self.angle[i][0]+self.motor_offset[0])
        self.move_motor_with_angle(self.servo_outer_pin,self.angle[i][1]+self.motor_offset[1])

    def move_motor_with_angle(self,motor,angle):
        wiringpi.pwmWrite(motor, int(100+angle/180*100))
        time.sleep(0.5)

    def move_motor(self,motor,value):
        wiringpi.pwmWrite(value)
        time.sleep(0.5)

    def set_random_order(self):
        # order = [1,2,3,4,5,6,7,8]
        self.foot_move_array = list(range(self.silk_start,self.silk_end))
        shuffle(self.foot_move_array)
        return self.foot_move_array

    def get_random_orfer(self):
        return self.foot_move_array

    def silk_out(self):
        self.motor_silk.ChangeDutyCycle(4.3+(120/180.0) * 5.0)

    def silk_in(self):
        self.motor_silk.ChangeDutyCycle(4.3+(20/180.0) * 5.0)

    def motor_init(self):
        self.move_motor_to_foot(0)
        self.silk_in()
        time.sleep(2)

    def detect_temp(self):
        result = []
        for index in self.get_random_orfer():
            print('Running to foot',index)
            self.move_motor_to_foot(index)
            temp = self.get_temp(self.thermo1,self.temp1_address)
            print('Temp : ',temp)
            result.append(temp)
        return result

    # if __name__ == '__main__':
    #     temp1 = get_temp(thermo1,temp1_address)
    #     print(temp1)

    #     print('System start!')
    #     #init
    #     motor_init()

    #     # running temp detect
    #     print(detect_temp())

    #     # running silk detect
    #     for index in get_random_order(1,9):
    #         print('Running to foot',index)
    #         move_motor_to_foot(index)
    #         silk_out()
    #         time.sleep(4)
    #         silk_in()
    #         time.sleep(0.5)
    


    