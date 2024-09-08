import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
import zipfile
import cv2
import shutil
import imagehash
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from collections import Counter
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def unzip_file(zip_path, extract_to_folder):
    if not os.path.exists(extract_to_folder):
        os.makedirs(extract_to_folder)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_folder)
        print(f"Files extracted to {extract_to_folder}")

unzip_file("./Original_Data.zip", "./")

# Function to check for duplicate images
def duplicate_data_check(class_dir):
    total = 0
    image_hashes = {}
        
    image_files = [f for f in os.listdir(class_dir) if f.endswith('.jpeg')]
        
    for image_file in image_files:
        image_path = os.path.join(class_dir, image_file)
            
        with Image.open(image_path) as img:
            img_hash = imagehash.average_hash(img)
            if img_hash in image_hashes:
                total += 1
            else:
                image_hashes[img_hash] = image_file

    print("There are ", total, "duplicates")

# Check for duplicates in dataset
print("Training set Normal check ")
duplicate_data_check("./Original_Data/train/NORMAL")
print("\nTraining set Pneumonia check ")
duplicate_data_check("./Original_Data/train/PNEUMONIA")
print("\nTesting set Normal check ")
duplicate_data_check("./Original_Data/test/NORMAL")
print("\nTesting set Pneumonia check ")
duplicate_data_check("./Original_Data/test/PNEUMONIA")

# Function to move images to new directory
def move_images(source_dir, destination_dir):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    for filename in os.listdir(source_dir):
        if filename.endswith(".jpeg"):
            source_path = os.path.join(source_dir, filename)
            destination_path = os.path.join(destination_dir, filename)
            shutil.copyfile(source_path, destination_path)

# Move images to model directory
move_images("./Original_Data/train/NORMAL", "./model_Data/NORMAL")
move_images("./Original_Data/test/NORMAL", "./model_Data/NORMAL")
move_images("./Original_Data/train/PNEUMONIA", "./model_Data/PNEUMONIA")
move_images("./Original_Data/test/PNEUMONIA", "./model_Data/PNEUMONIA")

# Function to remove duplicate images
def remove_duplicates(class_dir):
    removed_count = 0
    image_hashes = {}
    
    image_files = [f for f in os.listdir(class_dir) if f.endswith('.jpeg')]
    
    for image_file in image_files:
        image_path = os.path.join(class_dir, image_file)
        
        with Image.open(image_path) as img:
            img_hash = imagehash.average_hash(img)
            
            if img_hash in image_hashes:
                os.remove(image_path)
                removed_count += 1
            else:
                image_hashes[img_hash] = image_file
    
    print("Total duplicates removed:", removed_count)

# Remove duplicates from model directory
print("Normal remove duplicates")
remove_duplicates("./model_Data/NORMAL")
print("\nPneumonia remove duplicates")
remove_duplicates("./model_Data/PNEUMONIA")

# Function to create a DataFrame from the dataset
def creating_dataframe(dataset_dir):
    data = {'image_path': [], 'label': []}

    normal_dir = os.path.join(dataset_dir, 'NORMAL')
    for filename in os.listdir(normal_dir):
        if filename.endswith('.jpeg'):
            image_path = os.path.join(normal_dir, filename)
            data['image_path'].append(image_path)
            data['label'].append(0)  

    pneumonia_dir = os.path.join(dataset_dir, 'PNEUMONIA')
    for filename in os.listdir(pneumonia_dir):
        if filename.endswith('.jpeg'):
            image_path = os.path.join(pneumonia_dir, filename)
            data['image_path'].append(image_path)
            data['label'].append(1) 

    df = pd.DataFrame(data)
    return df

# Create DataFrame
df = creating_dataframe('./model_Data')

# Split the data
train_df, test_df = train_test_split(df, test_size=0.3)
train_df, val_df = train_test_split(train_df, test_size=0.3)

# Print distribution of training labels
label_counts = train_df['label'].value_counts()
count_label_N = label_counts.get(0, 0)
count_label_P = label_counts.get(1, 0)

print("Number of 'Normal' labels:", count_label_N)
print("Number of 'Pneumonia' labels:", count_label_P)

# Function to process images
def process_image(image_path, target_size=(224, 224)):
    img = cv2.imread(image_path)
    img = cv2.resize(img, target_size)
    img = img / 255.0 
    return img 

# Flatten images
def flatten_images(images):
    return images.reshape(images.shape[0], -1) 
# Reshape images back to original dimensions
def reshape_images(flattened_images, original_shape):
    return flattened_images.reshape(-1, *original_shape)

# Prepare training data
X_paths = train_df['image_path'].values
y = train_df['label'].values
X = np.array([process_image(path) for path in X_paths])

# Flatten images for SMOTE
X_flattened = flatten_images(X)

# Apply SMOTE
smote = SMOTE()
X_resampled_flattened, y_resampled = smote.fit_resample(X_flattened, y)

# Reshape back to original dimensions
X_resampled = reshape_images(X_resampled_flattened, (224, 224, 3))
del X_resampled_flattened
del X_flattened
del X
del y
del train_df
# Print new distribution of labels
label_counts = Counter(y_resampled)
print("Number of Normal labels after oversampling:", label_counts[0])
print("Number of Pneumonia labels after oversampling:", label_counts[1])

# Prepare validation data
X_paths_val = val_df['image_path'].values
yval = val_df['label'].values
X_val = np.array([process_image(path) for path in X_paths_val])

# Define and compile the model
model = Sequential([
    Conv2D(filters=64, kernel_size=3, activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    
    Conv2D(filters=64, kernel_size=2, activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(filters=128, kernel_size=3, activation='relu'),
    MaxPooling2D((2, 2)),
    
    Conv2D(filters=256, kernel_size=3, activation='relu'),
    MaxPooling2D((2, 2)),
    
    Flatten(),
    Dense(512, activation='relu'),
    
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# Train the model
history = model.fit(
    X_resampled, y_resampled,
    epochs=9,
    validation_data=(X_val, yval)
)

# Plot training & validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()

# Plot training & validation loss values
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()


model.save('model.h5')