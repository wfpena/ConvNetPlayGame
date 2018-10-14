import cv2
from mss import mss
import numpy as np
import keyboard
import os
import time

from test_sqlite.test_sqlite import SequenceImg

def preprocessing(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def empty_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

folder_path = r'./images10'

if not os.path.exists(folder_path):
    os.mkdir(folder_path)
# else:
#    empty_folder(folder_path)

sq = SequenceImg()

# Contando quantas imagens já existem no folder para
# colocar o current a partir desse número
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

    # if not os.path.exists(folder_path):
    #     os.mkdir(folder_path)
    #else:
    #    empty_folder(folder_path)

    with open(folder_path + '/actions.csv', 'a') as csv:
        x = 0
        space_pressed = False
        while True:
            img = preprocessing(np.array(sct.grab(coordinates)))

            if keyboard.is_pressed('space') and not space_pressed:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('space')
                sq.increment_sq()
                space_pressed = True
                #x += 1

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
                #x += 1

            if keyboard.is_pressed('q'):
                csv.close()
                cv2.destroyAllWindows()
                break

start()