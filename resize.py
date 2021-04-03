import sys
from PIL import Image

PICTURE = sys.argv[1]
COLOR = 255

image = Image.open('./raw/{}.jpg'.format(PICTURE))
print(image.mode)
print(image.size)
width, height = image.size
new_width = 2*height
left = (new_width - width)//2
image2 = Image.new('L', (new_width, height), color = COLOR)
image2.paste(image, (left,0))
print(image2.size)
print(image2.mode)
image2.save('./images/{}.jpg'.format(PICTURE))

