#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

from keras.models import Model
from keras.layers import Input
from keras.layers import Activation
import keras.backend as K
import tensorflow as tf

from NumPyNet.layers import cost_layer as cl
from NumPyNet.layers.cost_layer import Cost_layer

from keras.losses import mean_squared_error
from keras.losses import mean_absolute_error
from keras.losses import logcosh
from keras.losses import hinge

import numpy as np

__author__ = ['Mattia Ceccarelli', 'Nico Curti']
__email__ = ['mattia.ceccarelli3@studio.unibo.it', 'nico.curti2@unibo.it']
__package__ = 'Cost Layer testing'


def test_cost_layer():
  '''
  Tests:
        the fwd function of the cost layer.
        if the cost is the same for every cost_type (mse and mae)
        if the delta is correctly computed
  To be tested:
        _smoothing
        _threshold
        _ratio
        noobject_scale
        masked
        _seg
        _wgan
  '''
  np.random.seed(123)

  losses = [mean_absolute_error, mean_squared_error, logcosh]
            #, hinge] # derivative is ambigous

  for loss_function in losses :

    keras_loss_type = loss_function

    outputs = 100
    truth = np.random.uniform(low=0., high=1., size=(outputs,))
    inpt = np.random.uniform(low=0., high=1., size=(outputs,))

    inp = Input(shape=(inpt.size, ))
    x = Activation(activation='linear')(inp)
    model = Model(inputs=[inp], outputs=x)

    # an input layer to feed labels
    truth_tf = K.variable(truth)

    if   keras_loss_type is mean_squared_error:  cost = cl.cost_type.mse
    elif keras_loss_type is mean_absolute_error: cost = cl.cost_type.mae
    elif keras_loss_type is logcosh:             cost = cl.cost_type.logcosh
    elif keras_loss_type is hinge:               cost = cl.cost_type.hinge
    else:
      raise ValuError()

    numpynet_layer = Cost_layer(input_shape=inpt.shape, cost_type=cost,
                                scale=1., ratio=0., noobject_scale=1.,
                                threshold=0., smoothing=0.)

    keras_loss = K.eval(keras_loss_type(truth_tf, inpt))
    numpynet_layer.forward(inpt, truth)
    numpynet_loss = numpynet_layer.cost

    assert np.isclose(keras_loss, numpynet_loss, atol=1e-7)

    # BACKWARD

    # compute loss based on model's output and true labels
    if   keras_loss_type is mean_squared_error:
      loss = K.mean( K.square(truth_tf - model.output) )
    elif keras_loss_type is mean_absolute_error:
      loss = K.mean( K.abs(truth_tf - model.output) )
    elif keras_loss_type is logcosh:
      loss = K.mean( K.log(tf.math.cosh(truth_tf - model.output)))
    elif keras_loss_type is hinge:
      loss = K.maximum(1. - truth_tf * model.output, 0)
    else:
      raise ValuError()

    # compute gradient of loss with respect to inputs
    grad_loss = K.gradients(loss, [model.input])

    # create a function to be able to run this computation graph
    func = K.function(model.inputs + [truth_tf], grad_loss)
    keras_delta = func([np.expand_dims(inpt, axis=0), truth])

    numpynet_delta = numpynet_layer.delta

    assert np.allclose(keras_delta, numpynet_delta)

    # all passed

if __name__ == '__main__':

  test_cost_layer()
