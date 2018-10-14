import pickle
import cv2
import numpy as np
import datetime

im1 = cv2.imread('{1}/frame_{0}.jpg'.format(2, '../images8'))
im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
im1 = cv2.resize(im1, (0, 0), fx=0.5, fy=0.5)

im2 = cv2.imread('{1}/frame_{0}.jpg'.format(2, '../images8'))
im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
im2 = cv2.resize(im2, (0, 0), fx=0.5, fy=0.5)

print(datetime.timedelta(seconds=61))

#im = np.array(im, dtype='float').reshape(34320)
#cv2.imshow('Normal', im)
#k = cv2.waitKey(0)
#cv2.destroyAllWindows()

with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([im1, im2], f)

# Getting back the objects:
with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    im1, im2 = pickle.load(f)
    cv2.imshow('Image 1', im1)
    cv2.imshow('Image 2', im2)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
