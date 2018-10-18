import cv2
from mss import mss
import numpy as np
import keyboard
import os
import skimage.measure

from test_sqlite.test_sqlite import SequenceImg

'''
    This script is used to capture frames from the game,
    by pressing:
    a       -> Do nothing
    space   -> shooting (labeled 1 in a csv file called actions.csv)
    e       -> Create a frame with label 1 without actually shooting
    q       -> stop the script
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

folder_path = r'./game_frames'

if not os.path.exists(folder_path):
    os.mkdir(folder_path)

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
        space_pressed = False
        while True:
            img = preprocessing(np.array(sct.grab(coordinates)))

            if keyboard.is_pressed('space') and not space_pressed:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('space')
                sq.increment_sq()
                space_pressed = False

            # Press 'e' to hit a correct prediction but without actually shooting
            if keyboard.is_pressed('e'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('space - e')
                sq.increment_sq()

            if keyboard.is_pressed('d'):
                space_pressed = False

            if keyboard.is_pressed('r'):
                space_pressed = False

            if keyboard.is_pressed('a'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('0\n')
                print('nothing')
                sq.increment_sq()
                space_pressed = False

            if keyboard.is_pressed('q'):
                csv.close()
                cv2.destroyAllWindows()
                break

start()