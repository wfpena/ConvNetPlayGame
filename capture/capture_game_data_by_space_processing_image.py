import cv2
from mss import mss
import numpy as np
import keyboard
import os
import time
import skimage.measure

from test_sqlite.test_sqlite import SequenceImg

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
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

folder_path = r'./images15_one_and_zero'

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
                space_pressed = False
                #x += 1

                # cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img_before)
                # csv.write('0\n')
                # print('before')
                # sq.increment_sq()

            # Press 'e' to hit a correct prediction but without actually shooting
            if keyboard.is_pressed('e'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('space - e')
                sq.increment_sq()
                #space_pressed = True
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

            img_before = img

start()