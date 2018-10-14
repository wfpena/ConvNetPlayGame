import cv2
from mss import mss
import numpy as np
import keyboard
import os
import time

def preprocessing(img):
    img = img[::,75:615]
    img = cv2.Canny(img, threshold1=100, threshold2=200)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def empty_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

folder_path = r'./images2'

def start():

    sct = mss()

    coordinates = {
        'top': 150,
        'left': 430,
        'width': 490,
        'height': 550,
    }

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    else:
        empty_folder(folder_path)

    with open(folder_path + '/actions.csv', 'w') as csv:

        x = 0
        time.sleep(2)

        while True:
            img = preprocessing(np.array(sct.grab(coordinates)))

            if keyboard.is_pressed('space'):
                cv2.imwrite('{1}/frame_{0}.jpg'.format(x, folder_path), img)
                csv.write('1\n')
                print('space')
                x += 1

            else:
                cv2.imwrite('{1}/frame_{0}.jpg'.format(x, folder_path), img)
                csv.write('0\n')
                print('nothing')
                x += 1

            if keyboard.is_pressed('q'):
                csv.close()
                cv2.destroyAllWindows()
                break

#start()