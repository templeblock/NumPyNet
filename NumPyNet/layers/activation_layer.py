#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division
from __future__ import print_function

from NumPyNet.activations import Activations

import numpy as np

__author__ = ['Mattia Ceccarelli', 'Nico Curti']
__email__ = ['mattia.ceccarelli3@studio.unibo.it', 'nico.curti2@unibo.it']
__package__ = 'Activation Layer'


class Activation_layer(object):

  def __init__(self, activation=Activations):
    '''
    Activation layer

    Parameters :
      activation : activation function of the layer
    '''

    self.activation = activation.activate
    self.gradient = activation.gradient

    self.output, self.delta = (None, None)

  def __str__(self):
    batch, out_width, out_height, out_channels = self.out_shape()
    return 'activation                 {0:>4d} x{1:>4d} x{2:>4d} x{3:>4d}   ->  {0:>4d} x{1:>4d} x{2:>4d} x{3:>4d}'.format(
           batch, out_width, out_height, out_channels)

  def out_shape(self):
    return self.output.shape

  def forward(self, inpt, copy=True):
    '''
    Forward of the activation layer, apply the selected activation function to
    the input

    Parameters:
      inpt: the input to be activated
      copy: default value is True. If True make a copy of the input before
            applying the activation
    '''
    self.output = self.activation(inpt, copy=copy)
    self.delta = np.zeros(shape=self.output.shape)

    self.delta = np.ones(shape=self.out_shape())

  def backward(self, delta, copy=False):
    '''
    Compute the backward of the activation layer

    Parameter:
      delta : global error to be backpropagated
    '''

    self.delta *= self.gradient(self.output, copy=copy)
    delta[:] = self.delta


if __name__ == '__main__':

  import os

  import pylab as plt
  from PIL import Image

  from NumPyNet import activations

  activation_func = activations.Loggy()

  img_2_float = lambda im : ((im - im.min()) * (1./(im.max() - im.min()) * 1.)).astype(float)
  float_2_img = lambda im : ((im - im.min()) * (1./(im.max() - im.min()) * 255.)).astype(np.uint8)

  filename = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dog.jpg')
  inpt = np.asarray(Image.open(filename), dtype=float)
  inpt.setflags(write=1)
  inpt = img_2_float(inpt)
  # Relu activation constrain
  inpt = inpt * 2 - 1

  layer = Activation_layer(activation=activation_func)

  # FORWARD

  layer.forward(inpt)
  forward_out_byron = layer.output
  print(layer)

  # BACKWARD

  delta = np.empty(shape=inpt.shape)
  layer.backward(delta, copy=True)

  # Visualizations

  fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(10, 5))
  fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)

  fig.suptitle('Activation Layer\nfunction : {}'.format(activation_func.name))

  ax1.imshow(float_2_img(inpt))
  ax1.set_title('Original image')
  ax1.axis('off')

  ax2.imshow(float_2_img(layer.output))
  ax2.set_title("Forward")
  ax2.axis("off")

  ax3.imshow(delta)
  ax3.set_title('Backward')
  ax3.axis('off')

  plt.show()
