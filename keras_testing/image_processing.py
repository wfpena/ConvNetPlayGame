import cv2
from mss import mss
import numpy as np
import skimage.measure

sct = mss()

coordinates = {
    'top': 150,
    'left': 430,
    'width': 490,
    'height': 550,
}


def processing_img(im):
    im = skimage.measure.block_reduce(im, (4, 4), np.max)
    im = cv2.blur(im, (4, 4))
    _, im = cv2.threshold(im, 175, 250, cv2.THRESH_BINARY)
    #im = cv2.resize(im, dsize=(52,52), interpolation=cv2.INTER_CUBIC)
    return im

#image = cv2.imread('../images3/frame_42.jpg')

image = np.array(sct.grab(coordinates))
image = image[::, 75:615]

image = cv2.imread('{1}/frame_{0}.jpg'.format(10, '../images12'))

#image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#image = processing_img(image)
image = cv2.resize(image, dsize=(52,69), interpolation=cv2.INTER_CUBIC)
print(image.shape)
cv2.imshow('Normal', image)
k = cv2.waitKey(0)
cv2.destroyAllWindows()


