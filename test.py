import numpy as np
import time
from cozmo import robot
from cozmo import oled_face as oled
import cozmo

try:
    from PIL import Image
except:
    print("Need to install Python module Pillow. Try using pip for easy installation.")

pictures = ['one', 'two', 'three', 'rock', 'paper', 'scissors']
pics = {}
for p in pictures: 
    image = Image.open('./images/{}.jpg'.format(p))
    image = image.resize(oled.dimensions())
    pics[p] = oled.convert_image_to_screen_data(image)
    

def program(robot: robot.Robot):

    if robot.lift_height.distance_mm > 45:
        with robot.perform_off_charger():
            robot.set_lift_height(0.0).wait_for_completed()
    count = ['three', 'two', 'one']
    say = ['rock', 'paper', 'scissors']

    for i in range(3):
        robot.say_text(say[i])
        robot.display_oled_face_image(pics[count[i]], 1000, True).wait_for_completed()
    robot.say_text('shoot')
    robot.display_oled_face_image(pics['scissors'], 1000, True).wait_for_completed()
    time.sleep(2.0)

  

    for i in range(3):
        throw_input = input("Enter gesture (r / p / s): ")
        while throw_input not in ['r', 'p', 's']:
            print("Invalid input! Try again!")
            throw_input = input("Enter gesture (r / p / s): ")

        if  throw_input == 'r':
            robot.display_oled_face_image(pics['rock'], 1000, False)
    
        elif throw_input == 'p':
            robot.display_oled_face_image(pics['paper'], 1000, False)
         
        else:
            robot.display_oled_face_image(pics['scissors'], 1000, False)
           
cozmo.run_program(program)