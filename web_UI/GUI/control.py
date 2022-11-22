import time
from GUI.foothow_rasberrypi import *

class ControlSystem():

    GUI_action_lock = False
    test_mode = False

    current_pos = 0

    data = {
        'memberid': 1,
        'test': None,
        'temp': None
    }

    # tests = [
    #     [1, 2, 3, 4, 5],
    #     [3, 5, 6, 0, 1],
    #     [8, 2, 0, 4, 0],
    #     [1, 4, 2, 7, 0],
    #     [8, 6, 3, 0, 5]
    # ]

    current_test = []

    def __init__(self, tkroot):
        self.TKroot = tkroot
        self.pi_control = Foothow_Rasberrypi()

    def set_random_order(self):
        self.pi_control.set_random_order()

    def get_random_order(self):
        return self.pi_control.get_random_order()

    def get_temp(self):
        # get temperature
        self.data['temp'] = self.pi_control.detect_temp()
        time.sleep(200/1000)

    def arm_moving(self, /, current, target):
        # before moving, check if the silk is in
        self.pi_control.silk_in()
        
        self.pi_control.move_motor_to_foot(target)
        time.sleep(200/1000)
        
        if self.test_mode:
            self.pi_control.silk_out()

    def foot_pos_n_press(self, n):
        self.data['test'] += [n]

        if self.current_test == []:
            self.test_mode = False
            self.arm_moving(self.current_pos, target= 0)
            return

        self.arm_moving(current = self.current_pos, target = self.current_test[-1])
        
        self.current_test.pop()
