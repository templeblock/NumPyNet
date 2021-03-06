#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Little example on how to use the Network class to create a model and perform
a basic classification of the MNIST dataset
'''

#from NumPyNet.layers.input_layer import Input_layer
from NumPyNet.layers.connected_layer import Connected_layer
from NumPyNet.layers.convolutional_layer import Convolutional_layer
from NumPyNet.layers.maxpool_layer import Maxpool_layer
from NumPyNet.layers.softmax_layer import Softmax_layer
from NumPyNet.layers.dropout_layer import Dropout_layer
from NumPyNet.network import Network
from NumPyNet.optimizer import Adam
from NumPyNet.utils import to_categorical
from NumPyNet.metrics import accuracy_score

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

__author__ = ['Mattia Ceccarelli', 'Nico Curti']
__email__ = ['mattia.ceccarelli3@studio.unibo.it', 'nico.curti2@unibo.it']
__package__ = 'Example MNIST'

if __name__ == '__main__':

  digits = datasets.load_digits()
  X, y = digits.images, digits.target

  del digits

  # add channels to images
  X = np.asarray([[x, x, x] for x in X])
  X = X.transpose(0, 2, 3, 1)

  X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                      test_size=.33,
                                                      random_state=42)

  batch = 128
  num_classes = len(set(y))

  del X, y

  # normalization to [0, 1]
  X_train *= 1. / 255.
  X_test  *= 1. / 255.

  # reduce the size of the data set for testing
  ############################################

  train_size = 512
  test_size  = 300

  X_train = X_train[:train_size, ...]
  y_train = y_train[:train_size]
  X_test  = X_test[ :test_size,  ...]
  y_test  = y_test[ :test_size]

  ############################################

  n_train = X_train.shape[0]
  n_test  = X_test.shape[0]

  # transform y to array of dimension 10 and in 4 dimension
  y_train = to_categorical(y_train).reshape(n_train, 1, 1, -1)
  y_test  = to_categorical(y_test).reshape(n_test, 1, 1, -1)


  # Create the modeland training
  model = Network(batch=batch, input_shape=X_train.shape[1:])

  # model.add(Input_layer(input_shape=(batch, 32, 32, 3))) # not necessary if input_shape is given to Network
  model.add(Convolutional_layer(input_shape=(batch, 8, 8, 3),
                                size=3, filters=32, stride=1, pad=True,
                                activation='Relu'))
  model.add(Convolutional_layer(input_shape=(batch, 8, 8, 32),
                                size=3, filters=64, stride=1, pad=True,
                                activation='Relu'))
  model.add(Maxpool_layer(size=2, stride=1, padding=True))
  model.add(Dropout_layer(prob=0.25))
  model.add(Connected_layer(input_shape=(batch, 8, 8, 64),
                            outputs=128, activation='Relu'))
  model.add(Dropout_layer(prob=0.5))
  model.add(Connected_layer(input_shape=(batch, 1, 1, 128),
                            outputs=num_classes, activation='Linear'))
  model.add(Softmax_layer(spatial=True))

  print('*************************************')
  print('\n Total input dimension: {}'.format(X_train.shape), '\n')
  print('*************************************')

  model.compile(optimizer=Adam)
  model.summary()

  print('\n***********START TRAINING***********\n')

  # Fit the model on the training set

  model.fit(X=X_train, y=y_train, max_iter=5)

  print('\n***********END TRAINING**************\n')


  # Test the prediction

  out = model.predict(X=X_test)

  truth     = y_test.argmax(axis=3).ravel()
  predicted = out.argmax(axis=3).ravel()

  #print('True      label: ', truth)
  #print('Predicted label: ', predicted)

  # accuracy test
  print('Accuracy Score : {:.3f}'.format(accuracy_score(truth, predicted)))
