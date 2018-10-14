from keras.preprocessing.image import ImageDataGenerator
import pickle
import math
from collections import defaultdict
import numpy as np
import os
script_dir = os.path.dirname(os.path.realpath('__file__')) #<-- absolute dir the script is in
rel_path = "..//python_pickles//images8.pkl"
abs_file_path = os.path.join(script_dir, rel_path)
print(abs_file_path)

print("Restoring the saved state of the dataset")
print(os.path.getsize(r'C:\Users\User\github_repos\testTensorFlow\python_pickles\images8.pkl'))
with open('images8.pkl', 'rb') as f:
    dataset_restored = pickle.load(f)

total_ones = 0
for idx, a in enumerate(dataset_restored['test']['y_test']):
  #print(idx, a)
  total_ones = total_ones + a

print("TEST")
print("Total Ones: {0}  Total Sample: {1}".format(total_ones, idx))
print("{0} % zeros ".format(100-(total_ones*100)/(idx+1)))
print("{0} % ones ".format((total_ones*100)/(idx+1)))


full_dataset = defaultdict(dict)
full_dataset['x'] = np.concatenate([dataset_restored['train']['x_train'], dataset_restored['test']['x_test']])
full_dataset['y'] = np.concatenate([dataset_restored['train']['y_train'], dataset_restored['test']['y_test']])

print(full_dataset['y'] .__len__())

total_ones = 0
for idx, a in enumerate(full_dataset['y']):
  #print(idx, a)
  total_ones = total_ones + a

print("TEST")
print("Total Ones: {0}  Total Sample: {1}".format(total_ones, idx + 1))
print("{0} % zeros ".format(100-(total_ones*100)/(idx+1)))
print("{0} % ones ".format((total_ones*100)/(idx+1)))

randomize = np.arange(len(full_dataset['x']))
np.random.shuffle(randomize)

full_dataset['x'] = full_dataset['x'][randomize]
full_dataset['y'] = full_dataset['y'][randomize]

random_indexes = np.random.randint(full_dataset['x'].__len__(), size=6)

# for i in random_indexes:
#   IPython.display.display(PIL.Image.fromarray(full_dataset['x'][i]))
#   print("Output: {0}    Image Index: {1}".format(full_dataset['y'][i], i))

total = full_dataset['x'].__len__()
test = math.trunc(total * 0.2)
train = math.trunc(total * 0.8)

d = defaultdict(dict)
d['train']['x_train'] = full_dataset['x'][0:train]
d['train']['y_train'] = full_dataset['y'][0:train]
d['test'] = {"x_test": full_dataset['x'][train:train + test],
                    "y_test": full_dataset['y'][train:train + test]}

dataset = d


batch_size = 3



train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow(dataset['train']['x_train'].reshape(-1, 275, 208, 1), dataset['train']['y_train'], batch_size)
validation_generator = test_datagen.flow(dataset['test']['x_test'].reshape(-1, 275, 208, 1), dataset['test']['y_test'], batch_size)

print(validation_generator)