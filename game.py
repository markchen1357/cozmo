import numpy as np
import time

def disp_count_down():
    print("3, 2, 1, shoot!")
    # TODO: show count down

def disp_throw(throw):
    if throw == 0:
        print("Robot throws rock")
        # TODO: show rock 
    elif throw == 1:
        print("Robot throws paper")
        # TODO: show paper
    else:
        print("Robot throws scissor")
        # TODO: show scissor

def get_result(robot, human):
    if robot == (human + 1) % 3:
        return 0 # robot win
    elif human == robot:
        return 2 # tie
    else:
        return 1 # human win

def disp_result(result):
    if result == 0:
        print("You lose!")
        # TODO: show lose
    elif result == 1:
        print("You win!")
        # TODO: show win
    else:
        print("Tied!")
        # TODO: show tie

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