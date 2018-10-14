from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
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
    #im = cv2.resize(im, dsize=(52,69), interpolation=cv2.INTER_CUBIC)
    return im


initialize_weights = True

img_shape = [138, 104]

# model = Sequential()
# #model.add(Conv2D(32, (3, 3), input_shape=(110, 42, 1)))
# if initialize_weights:
#   print("Weights Initialized")
#   model.add(Conv2D(32, (3, 3), input_shape=(img_shape[0], img_shape[1], 1), kernel_initializer='random_uniform'))
# else:
#   print("Not initializing weights")
#   model.add(Conv2D(32, (3, 3), input_shape=(img_shape[0], img_shape[1], 1)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Conv2D(64, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Conv2D(128, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# model.add(Conv2D(256, (3, 3)))
# model.add(Activation('relu'))
# model.add(MaxPooling2D(pool_size=(2, 2)))
#
# # the model so far outputs 3D feature maps (height, width, features)
#
# model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
# #model.add(Dense(128*275*208))
# model.add(Dense(1000))
# model.add(Activation('relu'))
# model.add(Dropout(0.1))
# model.add(Dense(1))
# model.add(Activation('sigmoid'))
json_file = open('../keras_model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights('../keras_model/first_try.h5')

sct = mss()

coordinates = {
    'top': 150,
    'left': 430,
    'width': 490,
    'height': 550,
}

def start():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(r"C:\\Users\\User\\Desktop\\chromedriver.exe", chrome_options=options)
    driver.get("https://www.gameeapp.com/game-bot/ibBTDViUP")

    actions = ActionChains(driver)

    with driver as dv:
        while(True):
            image = np.array(sct.grab(coordinates))
            image = image[::, 75:615]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
            image = processing_img(image)

            p = model.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 1))
            print(p)
            if(p):
                print("aa", p)
                keyboard.press('space')
                actions.send_keys(Keys.SPACE).perform()

def start_no_driver():
    i = 0
    empty_folder('./imgs')
    while (True):
        image = np.array(sct.grab(coordinates))
        image = image[::, 75:615]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
        image = processing_img(image)

        p = model.predict_classes(image.reshape(-1, image.shape[0], image.shape[1], 1))
        print(p)

        if (p):
            print(i)
            cv2.imwrite('./imgs/frame_{0}.jpg'.format(i), image)
            i += 1
            print("aa", p)
            pyautogui.press('space')
            time.sleep(2)
            #keyboard.write('space', delay=0)


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
            #keyboard.write(' ',delay=0)
            pyautogui.press('space')
#test_input()

start_no_driver()
#test_keypress()