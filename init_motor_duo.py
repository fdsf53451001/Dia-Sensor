import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo1_pin = 12     # 外側
GPIO.setup(servo1_pin, GPIO.OUT)
motor1 = GPIO.PWM(servo1_pin, 50) # PWM with 50Hz
motor1.start(1) # Initialization

servo2_pin = 13     # 內側
GPIO.setup(servo2_pin, GPIO.OUT)
motor2 = GPIO.PWM(servo2_pin, 50) # PWM with 50Hz
motor2.start(1) # Initialization

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
    move_motor_with_angle(motor1,angle1)
    move_motor_with_angle(motor2,angle2)
    time.sleep(2)