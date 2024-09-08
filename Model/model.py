import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import cv2

#Using this to check for deplicates in the dataset
import imagehash

#For image transfering 
import shutil

#To deal with the imballance problem
from imblearn.over_sampling import SMOTE

#Model
import tensorflow as tf
from keras.models import Sequential
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing import image

#For Augmenting
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#For the confusion matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

from collections import Counter


