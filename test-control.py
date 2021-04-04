import numpy as np
import time
import sys
from functools import partial
from cozmo import robot
from cozmo import oled_face as oled
import cozmo


try:
    from PIL import Image
except:
    print("Need to install Python module Pillow. Try using pip for easy installation.")

ROBOT_VOICE = False
PICTURES = ['one', 'two', 'three', 'rock', 'paper', 'scissors']
SEED = 0
FILE = 'images'


def get_pictures():
    pics = {}
    for p in PICTURES: 
        image = Image.open('./{}/{}.jpg'.format(FILE, p))
        image = image.resize(oled.dimensions())
        pics[p] = oled.convert_image_to_screen_data(image)
    return pics

def disp_count_down(robot, pics):
    print("3, 2, 1, shoot!")
    # TODO: show count down
    count = ['three', 'two', 'one']
    say = ['rock', 'paper', 'scissors']

    for i in range(3):
        robot.say_text(say[i], use_cozmo_voice = ROBOT_VOICE)
        robot.display_oled_face_image(pics[count[i]], 1000, True).wait_for_completed()
    robot.say_text('shoot', use_cozmo_voice = ROBOT_VOICE) 

def disp_throw(robot, pics, throw, current): 
    throw_dict = ['rock', 'paper', 'scissors']
    symbol = throw_dict[throw]

    if current:
        if not current.is_completed:
            current.abort()

    print('Robot throws {}'.format(symbol))

    return robot.display_oled_face_image(pics['rock'], 50000, True)


def get_result(rob_res, hum_res):
    if rob_res == (hum_res + 1) % 3:
        return 0 # robot win
    elif hum_res == rob_res:
        return 2 # tie
    else:
        return 1 # human win

def say_result(robot, result):
    response_list = ['Yes, I win', 'Aw, you win', 'We have tied']
    response = response_list[result]
  
    robot.say_text(response, use_cozmo_voice = ROBOT_VOICE, in_parallel = True).wait_for_completed()
  


    
def program(robot):

    # rock = 0, paper = 1, scissor = 2
    gesture_dict = {'r': 0, 'p': 1, 's': 2}

    # conditions: control = 0, verbal cheat = 1, action cheat = 2
   
    #pictures
    pics = get_pictures()

    cur_throw = 0
    disp_count_down(robot, pics)
    first_display = disp_throw(robot, pics, cur_throw, None)
    human_throw_input = input("Enter human gesture (r / p / s): ")
    while human_throw_input not in ['r', 'p', 's']:
        print("Invalid input! Try again!")
        human_throw_input = input("Enter human gesture (r / p / s): ")
    human_throw = gesture_dict[human_throw_input]

    result = get_result(cur_throw, human_throw) 
    say_result(robot, result)
    

def main():

    cozmo.run_program(program)


if __name__ == '__main__':
    main()