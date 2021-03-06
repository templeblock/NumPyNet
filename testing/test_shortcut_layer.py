# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from keras.models import Model
from keras.layers import Input
from keras.layers import Activation
import keras.backend as K

from NumPyNet.layers.shortcut_layer import Shortcut_layer
from NumPyNet.activations import Relu
from NumPyNet.activations import Logistic
from NumPyNet.activations import Linear
from NumPyNet.activations import Tanh
from keras.layers import Add

import numpy as np

__author__ = ['Mattia Ceccarelli', 'Nico Curti']
__email__ = ['mattia.ceccarelli3@studio.unibo.it', 'nico.curti2@unibo.it']
__package__ = 'Shortcut Layer testing'


def test_shortcut_layer():
  '''
  Tests:
    shortcut layer forward
    shortcut layer backward
  to be:
  '''
  np.random.seed(123)

  alphas  = np.round(np.linspace(0, 1, 3), 2)
  betas   = np.round(np.linspace(0, 1, 3), 2)
  batches = [1, 5, 10]

  keras_activations = ['tanh','linear','relu', 'sigmoid']
  numpynet_activations = [Tanh, Linear, Relu, Logistic]

  for keras_activ, numpynet_activ in zip(keras_activations, numpynet_activations):
    for alpha in alphas:
      for beta in betas:
        for batch in batches:

          inpt1      = np.random.uniform(low=-1., high=1., size=(batch, 100, 100, 3))
          inpt2      = np.random.uniform(low=-1., high=1., size=(batch, 100, 100, 3))
          b, w, h, c = inpt1.shape

          # numpynet model
          numpynet = Shortcut_layer(activation=numpynet_activ,
                                    alpha=alpha, beta=beta)

          # Keras Model, double input
          inp1  = Input(shape=(w, h, c), batch_shape=inpt1.shape)
          inp2  = Input(shape=(w, h, c), batch_shape=inpt2.shape)
          x     = Add()([inp1,inp2])
          out   = Activation(activation=keras_activ)(x)
          model = Model(inputs=[inp1,inp2], outputs=out)

          # FORWARD

          # Perform Add() for alpha*inpt and beta*inpt
          forward_out_keras = model.predict([alpha*inpt1, beta*inpt2])

          numpynet.forward(inpt1,inpt2)
          forward_out_numpynet = numpynet.output

          assert forward_out_keras.shape == forward_out_numpynet.shape
          assert np.allclose(forward_out_keras, forward_out_numpynet, atol=1e-7)

          # BACKWARD

          grad = K.gradients(model.output, model.inputs)
          func = K.function(model.inputs + [model.output],grad)

          delta1, delta2 = func([alpha*inpt1, beta*inpt2])

          delta1 *= alpha
          delta2 *= beta

          delta      = np.zeros(shape=inpt1.shape, dtype=float)
          prev_delta = np.zeros(shape=inpt2.shape, dtype=float)

          numpynet.delta = np.ones(shape=(batch, w, h, c), dtype=float)
          numpynet.backward(delta, prev_delta)

          assert np.allclose(delta1, delta)
          assert np.allclose(delta2, prev_delta, atol=1e-8)

if __name__ == '__main__':

  test_shortcut_layer()
