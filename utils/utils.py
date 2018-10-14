import numpy as np
import os

class GameeUtils:
    def __init__(self):
        print("Starting Utils class")

    def get_percentages(self, folder_path='C:/Users/User/github_repos/testTensorFlow/images8'):
        labels = np.genfromtxt(folder_path + '/actions.csv', delimiter=',')
        total_ones = 0
        for idx, a in enumerate(labels):
            total_ones = total_ones + a

        print(total_ones, idx, (total_ones * 100) / (idx + 1))
        print("{0} % zeros ".format(100 - (total_ones * 100) / (idx + 1)))
        print("{0} % ones ".format((total_ones * 100) / (idx + 1)))
