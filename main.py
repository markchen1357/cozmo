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

PICTURES = ['one', 'two', 'three', 'rock', 'paper', 'scissors']
SEED = 0
FILE = 'images'
LOG = []
ROBOT_VOICE = False

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
  

    
def program(condition, robot):

    # rock = 0, paper = 1, scissor = 2
    gesture_dict = {'r': 0, 'p': 1, 's': 2}

    # conditions: control = 0, verbal cheat = 1, action cheat = 2
   
    # cheat rounds
    cheat_rounds = np.array([4, 8, 15])

    # total number of rounds
    n_round = 20

    #pictures
    pics = get_pictures()

    print("Game starts!")
    robot.say_text('Let us start the game', use_cozmo_voice = ROBOT_VOICE).wait_for_completed()
    time.sleep(2.0)

    # set seed to keep consistency for all participants
    np.random.seed(SEED)
    # sequence longer than 20 in case of extended interactions
    robot_throws = np.random.randint(3, size= 100) 

    cur = 0
    while (cur < n_round):
        second_display = None
        is_cheat_round = (cur+1) in cheat_rounds
        cur_throw = robot_throws[cur]

        if (condition and is_cheat_round):
            print("---- Round %d (cheat round) ----" %(cur+1))
        else:
            print("---- Round %d ----" %(cur+1))
        
        disp_count_down(robot, pics)
        first_display = disp_throw(robot, pics, cur_throw, None)

        human_throw_input = input("Enter human gesture (r / p / s): ")
        while human_throw_input not in ['r', 'p', 's']:
            print("Invalid input! Try again!")
            human_throw_input = input("Enter human gesture (r / p / s): ")
        LOG.append(human_throw_input)
        human_throw = gesture_dict[human_throw_input]

        # robot win = 0, human win = 1, tie = 2
        result = get_result(cur_throw, human_throw)

        if condition > 0 and is_cheat_round:
            if result == 0:
                # robot wins fairly. all rounds pushed back
                n_round += 1
                cheat_rounds += 1
            elif condition == 1:
                # verbal cheat
                result = 0
            elif condition == 2:
                # action cheat
                cur_throw = (human_throw + 1) % 3
                second_display = disp_throw(robot, pics, cur_throw, first_display)
                result = 0

        say_result(robot, result)
        if second_display:
            second_display.abort()
        cur += 1
        time.sleep(2) 
        
    print("Game ends!")
    robot.say_text('The game is finished', use_cozmo_voice = ROBOT_VOICE).wait_for_completed()

def main():

    DEBUG = False
    opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    if len(opts) > 0:
        if "-d" in opts:
            DEBUG = True
        else:
            raise SystemExit(f"Usage: {sys.argv[0]} (-d) <arguments>...")

    if len(args) == 0:
        print('Please specify condition as either [control/verbal-cheat/action-cheat]')
        sys.exit(0)

    if len(args) > 1:
        print('Too many arguments')
        sys.exit(0)

    if args[0] == 'control':
        CONDITION = 0
    elif args[0] == 'verbal-cheat':
        CONDITION = 1
    elif sys.argv[1] == 'action-cheat':
        CONDITION = 2
    else:
        print('Invalid condition. Please give condition as either [control/verbal-cheat/action-cheat]')
        sys.exit(0)

    if not DEBUG:
        NAME = input('Enter the partcipants name as [LAST-FIRST]: ')
        while ' ' in NAME:
            print('No whitespace in name')
            NAME = input('Enter the partcipants name as [LAST-FIRST]: ')

    cozmo_program = partial(program, CONDITION) 
    cozmo.run_program(cozmo_program)

    if not DEBUG:
        np.savetxt('./participants/{}-{}.csv'.format(NAME, sys.argv[1]), LOG, delimiter = ', ', fmt = '% s')


if __name__ == '__main__':
    main()