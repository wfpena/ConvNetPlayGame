import cv2
from mss import mss
import numpy as np
import skimage
from skimage import measure
from PIL import Image
import keyboard
from keras.models import model_from_json

import os
from capture_game_data import empty_folder

import time

import pyautogui
from keras import backend as K
K.set_image_dim_ordering('tf')

def processing_img(im):
    im = cv2.Canny(im, threshold1=100, threshold2=200)
    im = skimage.measure.block_reduce(im, (4, 4), np.max)
    im = cv2.blur(im, (4, 4))
    _, im = cv2.threshold(im, 175, 250, cv2.THRESH_BINARY)
    im = cv2.resize(im, dsize=(60, 77), interpolation=cv2.INTER_CUBIC)
    im = np.stack((im,) * 3, -1)
    return im

def processing_smaller(img):
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    img = skimage.measure.block_reduce(img, (4, 4), np.max)
    img = cv2.blur(img, (4, 4))
    _, img = cv2.threshold(img, 175, 250, cv2.THRESH_BINARY)
    img = cv2.resize(img, dsize=(52, 69), interpolation=cv2.INTER_CUBIC)
    img = np.stack((img,) * 3, -1)
    return img

model_number = ''
drive_path = '../../../Desktop/GoogleDrive/'

json_file = open(drive_path + 'model' + model_number + '.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(drive_path + 'first_try' + model_number + '.h5')

sct = mss()

coordinates = {
    'top': 150,
    'left': 430,
    'width': 490,
    'height': 550,
}

def start_no_driver():
    i = 0
    empty_folder('./imgs')
    while (True):
        image = np.array(sct.grab(coordinates))
        image = image[::, 75:615]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = processing_img(image)
        image = processing_smaller(image)

        p = model.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 3))    
        print(p)

        if (p):
            print(i)
            cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)
            i += 1
            print("aa", p)
            pyautogui.press('space')
            time.sleep(1.2)

#driver.close()

def test_image_sct(idx, folder_path):
    image = np.array(sct.grab(coordinates))
    image = image[::, 75:615]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    image = processing_img(image)
    print(type(image))
    im = Image.fromarray(image)
    im.save(folder_path + "/your_file_{0}.jpeg".format(idx))


def test_input():
    i = 0
    folder_path = './imgs'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    empty_folder(folder_path)
    while True:
        if keyboard.is_pressed('a'):
            test_image_sct(i, folder_path)
            i += 1

def test_keypress():
    print('Keypress test started')
    while True:
        if keyboard.is_pressed('a'):
            pyautogui.press('space')

# test_input()
start_no_driver()
# test_keypress()