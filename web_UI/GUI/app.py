from imghdr import tests
import tkinter as tk
from PIL import Image, ImageTk
import json
import random
from GUI.control import *

IMAGE_PATH = 'GUI/img/foot.jpg'

div_size = 200
align_mode = 'nswe' # align center
pad = 3

root = tk.Tk()
control = ControlSystem(root)
root.title('FootHow')
root.resizable(width = False, height = False)

root_div1 = tk.Frame(root, width = div_size * 1.5, height = div_size, bg = 'Coral') # 300 * 200
root_div2 = tk.Frame(root, width = div_size * 1.5, height = div_size * 2, bg = 'Khaki') # 300 * 400
root_div3 = tk.Frame(root, width = div_size * 3, height = div_size * 3, bg = 'green') # 600 * 600

root_div1.grid(column = 0, row = 0, padx = pad, pady = pad, sticky = align_mode)
root_div2.grid(column = 0, row = 1, padx = pad, pady = pad, sticky = align_mode)
root_div3.grid(column = 1, row = 0, rowspan = 2, padx = pad, pady = pad, sticky = align_mode)



start_temp_test_button_div1 = tk.Button(root_div1, text = 'Start temperature test', bg = 'white', fg = 'black')

temp_label_div2 = tk.Label(root_div2, text = 'temperature test: ', bg = 'white', fg = 'black')
nerve_label_div2 = tk.Label(root_div2, text = 'nerve function test: ', bg = 'white', fg = 'black')
send_button_div2 = tk.Button(root_div2, text = 'send', bg = 'white', fg = 'black')

canvas = tk.Canvas(root_div3, width = 600, height = 600)
start_nerve_test_button_div3 = tk.Button(root_div3, text = 'Start nerve test', bg = 'white', fg = 'black')
foot_pos_0 = tk.Button(root_div3, text = 'none', bg = 'gray', fg = 'black')
foot_pos_1 = tk.Button(root_div3, text = '1', bg = 'gray', fg = 'black')
foot_pos_2 = tk.Button(root_div3, text = '2', bg = 'gray', fg = 'black')
foot_pos_3 = tk.Button(root_div3, text = '3', bg = 'gray', fg = 'black')
foot_pos_4 = tk.Button(root_div3, text = '4', bg = 'gray', fg = 'black')
foot_pos_5 = tk.Button(root_div3, text = '5', bg = 'gray', fg = 'black')
foot_pos_6 = tk.Button(root_div3, text = '6', bg = 'gray', fg = 'black')
foot_pos_7 = tk.Button(root_div3, text = '7', bg = 'gray', fg = 'black')
foot_pos_8 = tk.Button(root_div3, text = '8', bg = 'gray', fg = 'black')



start_temp_test_button_div1.place(x = 75, y = 90, width = 150, height = 20)

temp_label_div2.place(x = 50, y = 160, width = 200, height = 20)
nerve_label_div2.place(x = 50, y = 190, width = 200, height = 20)
send_button_div2.place(x = 125, y = 220, width = 50, height = 20)

canvas.grid(column = 0, row = 0)
img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((600, 600), Image.ANTIALIAS))
canvas.background = img  # Keep a reference in case this code is put in a function.
bg = canvas.create_image(0, 0, anchor = tk.NW, image = img)

start_nerve_test_button_div3_window = canvas.create_window(245, 10, anchor = tk.NW, window = start_nerve_test_button_div3)
foot_pos_0_window = canvas.create_window(280, 40, anchor = tk.NW, window = foot_pos_0)
foot_pos_1_window = canvas.create_window(160, 30, anchor = tk.NW, window = foot_pos_1)
foot_pos_2_window = canvas.create_window(180, 150, anchor = tk.NW, window = foot_pos_2)
foot_pos_3_window = canvas.create_window(100, 130, anchor = tk.NW, window = foot_pos_3)
foot_pos_4_window = canvas.create_window(50, 190, anchor = tk.NW, window = foot_pos_4)
foot_pos_5_window = canvas.create_window(420, 30, anchor = tk.NW, window = foot_pos_5)
foot_pos_6_window = canvas.create_window(400, 150, anchor = tk.NW, window = foot_pos_6)
foot_pos_7_window = canvas.create_window(480, 130, anchor = tk.NW, window = foot_pos_7)
foot_pos_8_window = canvas.create_window(530, 190, anchor = tk.NW, window = foot_pos_8)



def update_GUI():
    global control

    temp_label_text = 'temperature test: ' + ('done' if control.data['temp'] else '')
    nerve_label_text = 'nerve function test: ' + ('done' if (control.data['test'] != None) and (len(control.data['test']) == 10) else '')

    temp_label_div2.config(text = temp_label_text)
    nerve_label_div2.config(text = nerve_label_text)

def start_temp_test_button_div1_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == False:
        control.GUI_action_lock == True
        control.get_temp()
        update_GUI()
        control.GUI_action_lock == False

def send_button_div2_press(event):
    global control

    if control.data['temp'] == None:
        return

    if control.data['test'] == None:
        return

    if control.GUI_action_lock == False and control.test_mode == False:
        control.GUI_action_lock == True

        print(json.dumps(control.data, indent = 4))

        control.data['temp'] = None
        control.data['test'] = None
        update_GUI()

        control.GUI_action_lock == False

def start_nerve_test_button_div3_press(event):
    global control

    if control.GUI_action_lock == False:
        control.GUI_action_lock == True
        control.test_mode = True

        # control.current_test = random.choice(control.tests).copy()
        # print(control.current_test)
        control.set_random_order()
        control.current_test = control.get_random_order()

        control.data['test'] = control.current_test.copy()

        control.arm_moving(current = control.current_pos, target = control.current_test[-1])
        control.current_test.pop()

        control.GUI_action_lock = False

def foot_pos_0_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(0)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_1_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(1)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_2_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(2)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_3_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(3)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_4_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(4)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_5_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(5)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_6_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(6)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_7_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(7)
        update_GUI()
        control.GUI_action_lock = False

def foot_pos_8_press(event):
    global control

    if control.GUI_action_lock == False and control.test_mode == True:
        control.GUI_action_lock == True
        control.foot_pos_n_press(8)
        update_GUI()
        control.GUI_action_lock = False



start_temp_test_button_div1.bind('<Button-1>', start_temp_test_button_div1_press)

send_button_div2.bind('<Button-1>', send_button_div2_press)

start_nerve_test_button_div3.bind('<Button-1>', start_nerve_test_button_div3_press)
foot_pos_0.bind('<Button-1>', foot_pos_0_press)
foot_pos_1.bind('<Button-1>', foot_pos_1_press)
foot_pos_2.bind('<Button-1>', foot_pos_2_press)
foot_pos_3.bind('<Button-1>', foot_pos_3_press)
foot_pos_4.bind('<Button-1>', foot_pos_4_press)
foot_pos_5.bind('<Button-1>', foot_pos_5_press)
foot_pos_6.bind('<Button-1>', foot_pos_6_press)
foot_pos_7.bind('<Button-1>', foot_pos_7_press)
foot_pos_8.bind('<Button-1>', foot_pos_8_press)


if __name__ == '__main__':
    root.mainloop()
