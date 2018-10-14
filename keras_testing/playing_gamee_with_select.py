import cv2
from mss import mss
import numpy as np
import skimage
from skimage import measure
from PIL import Image
import keyboard
from keras.models import model_from_json
from PIL import Image

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
    #im = cv2.resize(im, dsize=(52,69), interpolation=cv2.INTER_CUBIC)
    return im


initialize_weights = True

img_shape = [138, 104]

# json_file = open('../keras_model/model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model = model_from_json(loaded_model_json)
# model.load_weights('../keras_model/first_try.h5')

json_file = open('../keras_model/model_not_basic2.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('../keras_model/first_try_not_basic2.h5')

json_file = open('../keras_model/model_select3.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model_select = model_from_json(loaded_model_json)
model_select.load_weights('../keras_model/first_try_select3.h5')

# First Level
json_file = open('../keras_model/model_vgg_ones_zeros.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model_first_level = model_from_json(loaded_model_json)
model_first_level.load_weights('../keras_model/first_try_vgg_ones_zeros.h5')

# json_file = open('../keras_model/model_all.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model_first_level = model_from_json(loaded_model_json)
# model_first_level.load_weights('../keras_model/first_try_all.h5')


# json_file = open('../keras_model/model_first_level3.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model_first_level = model_from_json(loaded_model_json)
# model_first_level.load_weights('../keras_model/first_try_first_level3.h5')


# json_file = open('../keras_model/model.played_first_level.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# model_first_level = model_from_json(loaded_model_json)
# model_first_level.load_weights('../keras_model/first_try.played_first_level.h5')
from matplotlib import pyplot as plt

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
    pressed = False
    print('Start')
    while (True):
        pressed = False
        image = np.array(sct.grab(coordinates))
        image = image[::, 75:615]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        image = processing_img(image)
        # image = cv2.resize(image, dsize=(52, 69), interpolation=cv2.INTER_CUBIC)

        p = model_select.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 1))

        if p[0] == 0 or p[0] == 1 or p[0] == 4 :
            #print("Not Zero")
            pred = 0
            while(pred != 1):
                image = np.array(sct.grab(coordinates))
                image = image[::, 75:615]
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                image = processing_img(image)
                image = cv2.resize(image, dsize=(52, 69), interpolation=cv2.INTER_CUBIC)
                image = np.stack((image,)*3, -1)
                pred = model_first_level.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 3))
                if pred == 0:
                    pressed = False
                if (pred) and not pressed:
                    print("select: ", p)
                    pyautogui.press('space')
                    pressed = True
                    cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)
                    i += 1
                    time.sleep(1.2)
                    #cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)

            # print(i)
            #cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)
            #i += 1
            # print("aa", p)
            # pyautogui.press('space')
            # time.sleep(2)
            #keyboard.write('space', delay=0)
        else:
            #print("Not Zero")
            image = np.array(sct.grab(coordinates))
            image = image[::, 75:615]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            image = processing_img(image)
            image = cv2.resize(image, dsize=(52, 69), interpolation=cv2.INTER_CUBIC)

            pred = model.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 1))
            if pred == 0:
                pressed = False
            if (pred) and not pressed:
                print("select: ", p)
                pyautogui.press('space')
                cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)
                i += 1
                pressed = True
                time.sleep(1.2)
                #time.sleep(2)

start_no_driver()
