import cv2
from mss import mss
import numpy as np
import keyboard
import os
from test_sqlite.test_sqlite import SequenceImg
import skimage.measure

def preprocessing(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    img = skimage.measure.block_reduce(img, (4, 4), np.max)
    img = cv2.blur(img, (4, 4))
    _, img = cv2.threshold(img, 175, 250, cv2.THRESH_BINARY)
    img = cv2.resize(img, dsize=(60, 77), interpolation=cv2.INTER_CUBIC)
    return img

def preprocessing_smaller(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    img = skimage.measure.block_reduce(img, (4, 4), np.max)
    img = cv2.blur(img, (4, 4))
    _, img = cv2.threshold(img, 175, 250, cv2.THRESH_BINARY)
    img = cv2.resize(img, dsize=(52, 69), interpolation=cv2.INTER_CUBIC)
    return img


def empty_folder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

folder_path = r'./images5'
folder_path = './images15_one_and_zero_smaller'
if not os.path.exists(folder_path):
    os.mkdir(folder_path)


#empty_folder(folder_path)


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

    with open(folder_path + '/actions.csv', 'a') as csv:
        space_pressed = False
        while True:
            # img = preprocessing(np.array(sct.grab(coordinates)))
            img = preprocessing_smaller(np.array(sct.grab(coordinates)))
            if keyboard.is_pressed('a'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('0\n')
                print('nothing')
                space_pressed = False
                sq.increment_sq()

            if keyboard.is_pressed('space') and not space_pressed:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(sq.get_current(), folder_path), img)
                csv.write('1\n')
                print('nothing')
                space_pressed = True
                sq.increment_sq()

            if keyboard.is_pressed('r'):
                space_pressed = False

            if keyboard.is_pressed('d'):
                space_pressed = False

            if keyboard.is_pressed('q'):
                csv.close()
                cv2.destroyAllWindows()
                break

start()