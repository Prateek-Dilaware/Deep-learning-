# -*- coding: utf-8 -*-
"""catvsdog_classsifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uPRKrDGGDjWLdfFbQY4HVBOngvrfiuW_
"""

!pip install opendatasets

"""Kaggle API :-

User Name - prateekdilaware
key - 4d88f228b5de483397a2ab5f8ecc8bbe
"""

import opendatasets as od
od.download("https://www.kaggle.com/datasets/salader/dogs-vs-cats")

import tensorflow as tf
from tensorflow import keras
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout

# generator - one for training data and one for validation data

train_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/dogs-vs-cats/train',
    labels = 'inferred',
    label_mode = 'int', # cat -0 , dog -1
    batch_size = 32,
    image_size = (256,256)
)

validation_ds = keras.utils.image_dataset_from_directory(
    directory = '/content/dogs-vs-cats/test',
    labels = 'inferred',
    label_mode = 'int',
    batch_size = 32,
    image_size = (256,256)
)

"""Certainly! The selected code uses the image_dataset_from_directory function from the keras.utils module to create training and validation datasets from the image files in the specified directories.

Here's a breakdown:

keras.utils.image_dataset_from_directory: This function is a convenient way to load image data from a directory structure where subdirectories represent different classes.
directory: This argument specifies the path to the root directory containing the image data. The function will look for subdirectories within this path, treating each subdirectory name as a class label.
labels='inferred': This tells the function to automatically infer the class labels from the subdirectory names.
label_mode='int': This specifies that the labels should be encoded as integers (e.g., 0 for the first class, 1 for the second, and so on). In this case, 'cat' will be 0 and 'dog' will be 1.
batch_size=32: This sets the number of images to include in each batch of data. The model will be trained on these batches.
image_size=(256, 256): This resizes all images to a consistent size of 256x256 pixels. This is important because neural networks typically require fixed-size input.
The code creates two datasets: train_ds from the /content/dogs-vs-cats/train directory and validation_ds from the /content/dogs-vs-cats/test directory. These datasets are then ready to be used for training and validating a deep learning model.
"""

# Normalize
def process(image,label):
  image = tf.cast(image/255. ,tf.float32)
  return image,label

train_ds = train_ds.map(process)
validation_ds = validation_ds.map(process)

"""This code defines a function process that takes an image and its corresponding label as input. Inside the function, it converts the image data to a floating-point type and scales the pixel values from the original range (0-255) to a range between 0 and 1 by dividing by 255. This normalization is a common preprocessing step in image processing for neural networks. The function then returns the normalized image and its label.

After defining the function, the code applies this process function to both the train_ds and validation_ds datasets using the .map() method. This means that for every element (image and label pair) in these datasets, the process function will be applied, effectively normalizing all the images in both the training and validation sets.


why we need to normalize here ?
 Normalization is a crucial step in preparing image data for training deep learning models like the one you're building. Here's why it's important:

Improved Training Stability: Neural networks are sensitive to the scale of input data. If the pixel values are large (0-255), the gradients during training can become very large, leading to unstable training and difficulty in converging to an optimal solution. Normalizing to a smaller range (0-1) helps to keep the gradients in a more manageable range, making the training process more stable.
Faster Convergence: By scaling the input features to a similar range, normalization helps the optimization algorithm (like gradient descent) converge faster. Without normalization, features with larger values might dominate the learning process, while features with smaller values might have less impact, even if they are equally important.
Better Performance: Normalization can lead to better overall model performance. When features are on a similar scale, the model can learn the relationships between them more effectively.
In the case of image data, normalizing the pixel values to a range of 0 to 1 (or sometimes -1 to 1) is a standard practice that helps theneural network learn more efficiently and achieve netter results.
"""

# Create CNN model

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3))) # 32 filters
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

#flatten layer
model.add(Flatten())

#Fully Connected layer

model.add(Dense(128,activation='relu'))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer="adam",loss= "binary_crossentropy",metrics=["accuracy"])

history= model.fit(train_ds,epochs=10,validation_data=validation_ds)

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

# Means there is overfitting

#Ways to reduce overfitting

# Data Augmentation
# L1/L2 regualrizer
# Dropout
#Batch Norm
# reduce Model Complexity

# We are using dropout and batch Norm

# Improving the CNN model

model = Sequential()

model.add(Conv2D(32,kernel_size=(3,3),padding='valid',activation='relu',input_shape=(256,256,3))) # 32 filters
model.add(BatchNormalization()),
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

model.add(Conv2D(64,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization()),
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

model.add(Conv2D(128,kernel_size=(3,3),padding='valid',activation='relu'))
model.add(BatchNormalization()),
model.add(MaxPooling2D(pool_size=(2,2),strides =2,padding='valid'))

#flatten layer
model.add(Flatten())

#Fully Connected layer

model.add(Dense(128,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(1,activation='sigmoid'))

model.summary()

model.compile(optimizer="adam",loss= "binary_crossentropy",metrics=["accuracy"])

history = model.fit(train_ds,epochs=10,validation_data=validation_ds)

import matplotlib.pyplot as plt
plt.plot(history.history['accuracy'],color='red',label='train')
plt.plot(history.history['val_accuracy'],color='blue',label='validation')
plt.legend()
plt.show()

plt.plot(history.history['loss'],color='red',label='train')
plt.plot(history.history['val_loss'],color='blue',label='validation')
plt.legend()
plt.show()

"""# Prediction"""

import cv2

test_img = cv2.imread('/content/dog.jpg')
plt.imshow(test_img)
plt.show()

test_img.shape

test_img = cv2.resize(test_img,(256,256))

test_input = test_img.reshape((1,256,256,3)) # Means we have only 1 img in our batch of this dimension

model.predict(test_input)

# One means dog

