from tkinter import *
import tkinter as tk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

def save_array2csv():
    print("Saving...")
    os.remove(folder_path +  '/actions.csv')
    with open(folder_path + '/actions.csv', 'a') as csv:
        for n in labels:
            csv.write('{0}\n'.format(n))
        print("Saved!")


# Variables
folder_path = './images5'
#folder_path = './images12_smaller'

folder_path = './images15_one_and_zero_smaller'

labels = np.genfromtxt(folder_path + '/actions.csv', delimiter=',')
i = 0

total_images = len(labels) - 1
current_image = i

total  = 0
for f in os.listdir(folder_path):
    if(os.path.splitext(f)[1][1:] == 'jpg'):
        total = total + 1

if total != total_images + 1:
    print('Images: ', total)
    print('Total labels: ', total_images + 1)
    raise Exception('Images and labels have different lengths!')

def change_value():
    if txt.get() == '1.0':
        current_value.set('0.0')
    elif txt.get() == '0.0':
        current_value.set('1.0')

    labels[i] = current_value.get()

def next(lbl, txt):
    global i
    i += 1
    if i > total - 1:
        i = 0

    current_value.set(labels[i])
    img = cv2.imread('{1}/frame_{0}.jpg'.format(i , folder_path))
    print("Shape ", img.shape) # (69, 52, 3)
    img = cv2.resize(img, dsize=(100, 111), interpolation=cv2.INTER_CUBIC)

    lbl_total_current.configure(text='Current: ' + str(i) + ' / ' + str(total_images))

    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

def prev(lbl, txt):
    global i
    i -= 1
    if i < 0:
        i = total - 1

    current_value.set(labels[i])
    img = cv2.imread('{1}/frame_{0}.jpg'.format(i , folder_path))
    img = cv2.resize(img, dsize=(100, 111), interpolation=cv2.INTER_CUBIC)

    lbl_total_current.configure(text='Current: ' + str(i) + ' / ' + str(total_images))

    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

def remove_image():
    global i
    global total
    global total_images
    global labels

    label_to_delete = i

    labels = np.delete(labels, i)
    save_array2csv()
    total_images = len(labels) - 1
    os.remove('{1}/frame_{0}.jpg'.format(i , folder_path))

    total = 0
    for f in os.listdir(folder_path):
        if (os.path.splitext(f)[1][1:] == 'jpg'):
            total = total + 1
    i -= 1
    if i < 0:
        i = total - 1

    total_images = len(labels) - 1
    lbl_total_current.configure(text='Current: ' + str(i) + ' / ' + str(total_images))

    for n in range(label_to_delete, total):
        os.rename('{1}/frame_{0}.jpg'.format(n + 1 , folder_path), '{1}/frame_{0}.jpg'.format(n , folder_path))

    current_value.set(labels[i])
    img = cv2.imread('{1}/frame_{0}.jpg'.format(i , folder_path))
    img = cv2.resize(img, dsize=(100, 111), interpolation=cv2.INTER_CUBIC)

    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img


window = Tk()

window.title("Creating the Dataset - Space Traveler")
window.geometry('370x200')

img = cv2.imread('{1}/frame_{0}.jpg'.format(i, folder_path))
img = cv2.resize(img, dsize=(100, 111), interpolation=cv2.INTER_CUBIC)

current_value = tk.StringVar()
current_value.set(labels[i])

img = Image.fromarray(img)

img = ImageTk.PhotoImage(img)
lbl = Label(window, text="Hello", image = img)

lbl.grid(column=0, row=0)

txt = Entry(window, width=10, textvariable=current_value, state='disabled')
txt.grid(column=4, row=0)

btn = Button(window, text="Next", command=lambda: next(lbl, txt))
btn.grid(column=1, row=1)

btn = Button(window, text="Prev", command=lambda: prev(lbl, txt))
btn.grid(column=0, row=1)

# Delete Image
btn = Button(window, text="Delete", command=lambda: remove_image())
btn.grid(column=0, row=4)


lbl_total_current = Label(window, text='Current: ' + str(current_image) + ' / ' + str(total_images)) #shows as text in the window
lbl_total_current.grid(column=2, row=3)

btn = Button(window, text="Change", command=lambda: change_value())
btn.grid(column=5, row=0)

btn = Button(window, text="Save", command=lambda: save_array2csv())
btn.grid(column=2, row=4)

window.mainloop()
