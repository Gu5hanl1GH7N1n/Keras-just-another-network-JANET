from __future__ import print_function
import os
import numpy as np

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam

from janet import JANET

batch_size = 100
num_classes = 10
epochs = 100
hidden_units = 128

learning_rate = 1e-3

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], -1, 1)
x_test = x_test.reshape(x_test.shape[0], -1, 1)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')

x_train = (x_train -  x_train.mean(axis=0, keepdims=True)) / (x_train.std(axis=0, keepdims=True) + 1e-8)
x_test = (x_test - x_test.mean(axis=0, keepdims=True)) / (x_test.std(axis=0, keepdims=True) + 1e-8)

print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


print('Evaluate IRNN...')
model = Sequential()
model.add(JANET(hidden_units,  input_shape=x_train.shape[1:]))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

rmsprop = Adam(lr=learning_rate, amsgrad=True)

model.compile(loss='categorical_crossentropy',
              optimizer=rmsprop,
              metrics=['accuracy'])

# model.fit(x_train, y_train,
#           batch_size=batch_size,
#           epochs=epochs,
#           verbose=1,
#           validation_data=(x_test, y_test),
#           callbacks=[ModelCheckpoint('weights/imdb_janet_mnist.h5', monitor='val_acc',
#                                      save_best_only=True, save_weights_only=True, mode='max')])

model.load_weights('weights/imdb_janet_mnist.h5')

scores = model.evaluate(x_test, y_test, verbose=1)
print('IndRNN test score:', scores[0])
print('IndRNN test accuracy:', scores[1])
