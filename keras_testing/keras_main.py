from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
import cv2

from keras import backend as K
K.set_image_dim_ordering('tf')


model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(110, 42, 1)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# the model so far outputs 3D feature maps (height, width, features)

model.add(Flatten())  # this converts our 3D feature maps to 1D feature vectors
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.load_weights('../keras_model/first_try.h5')

for i in range(10):
    image = cv2.imread('../images2/frame_{}.jpg'.format(i))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (0, 0), fx=0.1, fy=0.2)
    # first_image = mnist.train.images[i]
    #first_image = np.array(image, dtype='float').reshape(1, 34320)
    # print_image(first_image)
    print(i)
    a = model.predict_classes(image.reshape(-1, 110, 42, 1)) #pred, {x: first_image})
    print(a)
