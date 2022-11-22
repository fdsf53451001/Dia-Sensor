import RPi.GPIO as GPIO
import time

import time
import wiringpi

GPIO.setmode(GPIO.BCM)
servo1_pin = 12     # 外側
servo2_pin = 13     # 內側

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(servo1_pin, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(servo2_pin, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)


print('Setup ready!')

def move_motor_with_angle(motor,angle):
    # dutycycle = ((angle/180.0) + 1.0) * 5.0
    dutycycle = 4.3+(angle/180.0) * 5.0
    motor.ChangeDutyCycle(dutycycle)
    time.sleep(0.5)

while True:
    print('Input angle (inner,outter):')
    angle2 = int(input())
    angle1 = int(input())
    wiringpi.pwmWrite(servo1_pin, int(100+angle1/180*100))
    wiringpi.pwmWrite(servo2_pin, int(100+angle2/180*100))
    time.sleep(2)