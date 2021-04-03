import numpy as np
import time
from cozmo import robot
from cozmo import oled_face as oled
import cozmo
try:
    from PIL import Image
except:
    print("Need to install Python module Pillow. Try using pip for easy installation.")

pictures = ['one', 'two', 'three']
pics = {}
for p in pictures: 
    image = Image.open('./images/{}.jpg'.format(p))
    image = image.resize(oled.dimensions())
    pics[p] = oled.convert_image_to_screen_data(image)
    

def program(robot: robot.Robot):
    robot.display_oled_face_image(pics['three'], 500, False)
    robot.display_oled_face_image(pics['two'], 500, False)
    robot.display_oled_face_image(pics['one'], 500, False)


cozmo.run_program(program)