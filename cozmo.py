import numpy as np
import time
from cozmo import robot
from cozmo import oled_face as oled
import cozmo
try:
    from PIL import Image
except:
    print("Need to install Python module Pillow. Try using pip for easy installation.")

class RPS:

    def __init__(self):
        self.robot = robot.Robot()

    def convert_pictures(self, picture):

    def convert_pictures(self, robot):
        pictures = ['one', 'two', 'three', 'rock', 'paper', 'scissors']
        pics = {}
        for p in pictures: 
            image = Image.open('./images/{}.png'.format(p))
            image = Image.resize(oled.dimensions(), Image.NEAREST)
            pics[p] = oled.convert_image_to_screen_data(image)
        self.dict = pics
    def disp_count_down(self, robot):
        print("3, 2, 1, shoot!")
        # TODO: show count down
        robot.display_oled_face_image(self.three, 500, False)
        robot.display_oled_face_image(self.two, 500, False)
        robot.display_oled_face_image(self.one, 500, False)


    def disp_throw(self, robot, throw):        
        if throw == 0:
            print("Robot throws rock")
            # TODO: show rock 
            robot.display_oled_face_image(self.rock, 500, False)
        elif throw == 1:
            print("Robot throws paper")
            # TODO: show paper
            robot.display_oled_face_image(self.paper, 500, False)
        else:
            print("Robot throws scissor")
            # TODO: show scissor
            robot.display_oled_face_image(self.scissors, 500, False)

    def disp_result(self, robot, rob_res, hum_res):
        if rob_res == (hum_res + 1) % 3:
            # robot win
            robot.say_text("I win", num_retries = 2)
        elif human == robot:
            # tie
            robot.say_text("It is a tie", num_retries = 2)
        else:
            # human win
            robot.say_text("You win", num_retries = 2)

   

    def program(self, robot):
        # rock = 0, paper = 1, scissor = 2
    gesture_dict = {'r': 0, 'p': 1, 's': 2}

    # control = 0, verbal cheat = 1, action cheat = 2
    condition = 1

    # cheat rounds
    cheat_rounds = np.array([4, 8, 15])

    # total number of rounds
    n_round = 20

    print("Game starts!")

    # set seed to keep consistency for all participants
    np.random.seed(0)
    # sequence longer than 20 in case of extended interactions
    robot_throws = np.random.randint(3, size=50) 

    cur = 1
    while (cur <= n_round):
        is_cheat_round = cur in cheat_rounds
        cur_throw = robot_throws[cur - 1]

        if (is_cheat_round):
            print("---- Round %d (cheat round) ----" %(cur))
        else:
            print("---- Round %d ----" %(cur))
        
        disp_count_down()
        disp_throw(cur_throw)

        human_throw_input = input("Enter human gesture (r / p / s): ")
        while human_throw_input not in ['r', 'p', 's']:
            print("Invalid input! Try again!")
            human_throw_input = input("Enter human gesture (r / p / s): ")
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
                disp_throw(cur_throw)
                result = 0

        time.sleep(2) # hold gesture image for a while
        disp_result(result)
        time.sleep(2) # hold result image for a while
        
        cur += 1
    
    print("Game ends!")

def main():
    # rock = 0, paper = 1, scissor = 2
    gesture_dict = {'r': 0, 'p': 1, 's': 2}

    # control = 0, verbal cheat = 1, action cheat = 2
    condition = 1

    # cheat rounds
    cheat_rounds = np.array([4, 8, 15])

    # total number of rounds
    n_round = 20

    print("Game starts!")

    # set seed to keep consistency for all participants
    np.random.seed(0)
    # sequence longer than 20 in case of extended interactions
    robot_throws = np.random.randint(3, size=50) 

    cur = 1
    while (cur <= n_round):
        is_cheat_round = cur in cheat_rounds
        cur_throw = robot_throws[cur - 1]

        if (is_cheat_round):
            print("---- Round %d (cheat round) ----" %(cur))
        else:
            print("---- Round %d ----" %(cur))
        
        disp_count_down()
        disp_throw(cur_throw)

        human_throw_input = input("Enter human gesture (r / p / s): ")
        while human_throw_input not in ['r', 'p', 's']:
            print("Invalid input! Try again!")
            human_throw_input = input("Enter human gesture (r / p / s): ")
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
                disp_throw(cur_throw)
                result = 0

        time.sleep(2) # hold gesture image for a while
        disp_result(result)
        time.sleep(2) # hold result image for a while
        
        cur += 1
    
    print("Game ends!")



if __name__ == '__main__':
    main()