import cv2
from mss import mss
import numpy as np
import keyboard
import os
import skimage.measure

from test_sqlite.test_sqlite import SequenceImg

'''
    This is used to capture different types of courses in the game
    and label between 5 types, that will be labeled from 0 to 4
    according to the key that is pressed
'''

def preprocessing(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    img = skimage.measure.block_reduce(img, (4, 4), np.max)
    img = cv2.blur(img, (4, 4))
    _, img = cv2.threshold(img, 175, 250, cv2.THRESH_BINARY)
    #im = cv2.resize(im, dsize=(52,52), interpolation=cv2.INTER_CUBIC)
    return img

def empty_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

folder_path = r'./game_course_types'

if not os.path.exists(folder_path):
    os.mkdir(folder_path)
# else:
#    empty_folder(folder_path)

sq = SequenceImg()

# Counting the number of images already in the folder
x = 0
for f in os.listdir(folder_path):
    if(os.path.splitext(f)[1][1:] == 'jpg'):
        x = x + 1

sq.set_current(x)
print('Current Index:', x)

def start():

    sct = mss()

    coordinates = {
        'top': 150,
        'left': 430,
        'width': 490,
        'height': 550,
    }

    with open(folder_path + '/actions.csv', 'a') as csv:
        x = 0
        space_pressed = False
        while True:
            img = preprocessing(np.array(sct.grab(coordinates)))

            if keyboard.is_pressed('0') and not space_pressed:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('0\n')
                print('0')
                sq.increment_sq()
                space_pressed = False

            if keyboard.is_pressed('1') and not space_pressed:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('1')
                sq.increment_sq()
                space_pressed = False

            if keyboard.is_pressed('2'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('2\n')
                print('Two')
                sq.increment_sq()

            if keyboard.is_pressed('3'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('3\n')
                print('Three')
                sq.increment_sq()
                space_pressed = False

            if keyboard.is_pressed('4'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('4\n')
                print('Three')
                sq.increment_sq()
                space_pressed = False

            if keyboard.is_pressed('q'):
                csv.close()
                cv2.destroyAllWindows()
                break

start()