import os
from capture_game_data import empty_folder
import cv2
import numpy as np
import shutil

#folder_to_read = '../images_not_basic'
folder_to_read = '../images12'
files = os.listdir(folder_to_read)
total =  len(files) - 1

print(total)

#folder_to_create = './images_not_basic_smaller'
folder_to_create = folder_to_read[1:] + '_smaller'
print(folder_to_create)
empty_folder(folder_to_create)
shutil.copy(folder_to_read + '/actions.csv', folder_to_create + '/actions.csv')
for i in range(total):
    im = cv2.imread('{1}/frame_{0}.jpg'.format(i, folder_to_read))
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = cv2.resize(im, dsize=(52,69), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(folder_to_create + '/frame_{0}.jpg'.format(i), im)