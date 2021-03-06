| **Author**   | **Project** | **Documentation**                                                                   | **Build Status**              |
|:------------:|:-----------:|:-----------------------------------------------------------------------------------:|:-----------------------------:|
|   [**N. Curti**](https://github.com/Nico-Curti) <br/> [**M. Ceccarelli**](https://github.com/Mat092)   |  **NumPyNet**  | [![docs](https://img.shields.io/badge/documentation-latest-blue.svg?style=plastic)](https://nico-curti.github.io/NumPyNet/) | **Linux/MacOS** : [![travis](https://travis-ci.com/Nico-Curti/NumPyNet.svg?branch=master)](https://travis-ci.com/Nico-Curti/NumPyNet) <br/> **Windows** : [![appveyor](https://ci.appveyor.com/api/projects/status/qbn3ml2q04j9rbat?svg=true)](https://ci.appveyor.com/project/Nico-Curti/numpynet) |

[![GitHub pull-requests](https://img.shields.io/github/issues-pr/Nico-Curti/NumPyNet.svg?style=plastic)](https://github.com/Nico-Curti/NumPyNet/pulls)
[![GitHub issues](https://img.shields.io/github/issues/Nico-Curti/NumPyNet.svg?style=plastic)](https://github.com/Nico-Curti/NumPyNet/issues)

[![GitHub stars](https://img.shields.io/github/stars/Nico-Curti/NumPyNet.svg?label=Stars&style=social)](https://github.com/Nico-Curti/NumPyNet/stargazers)
[![GitHub watchers](https://img.shields.io/github/watchers/Nico-Curti/NumPyNet.svg?label=Watch&style=social)](https://github.com/Nico-Curti/NumPyNet/watchers)

<a href="https://github.com/UniboDIFABiophysics">
<div class="image">
<img src="https://cdn.rawgit.com/physycom/templates/697b327d/logo_unibo.png" width="90" height="90">
</div>
</a>

# Neural Networks in Pure NumPy - NumPyNet

Implementation in **pure** numpy of neural networks models. This library is usefull as testing framework for optimized codes.

## Table of Contents
1. [Introduction](#introduction)
2. [Layers](#layers)
3. [Installation](#installation)
4. [Authors](#authors)
5. [License](#license)
6. [Contributions](#contributions)
7. [Acknowledgment](#acknowledgment)
8. [Citation](#citation)

### Introduction

**TODO:** Insert here introduction about neural network models starting from the Simple Perceptron model provided [here](https://gist.github.com/Nico-Curti/358b7a2ffed1abbb57ee87a5338ca073)

Layers are the main core of a Neural Network model: every one of them performs, on its respective input, a different operation.
The concatenation of multiple Layer form a CNN, where for concatenation we mean that the output of a layer become the input of the next one.

In the NumPyNet framework a Layer is a python `class`, this allow the users to instantiate an object of the chosen type and call one of its methods.

Main Method:

* **forward** : this function is defined for every Layer and perform the so-called *forward pass*, that is the implementation of the transformation the Layer performs on the Input.
It usually receives as argument just the output of the previous Layer

* **backward** : this function is defined for every Layer and perform the so-called *backward pass*, that is an implementation of the BackPropagation algorithm for the error.
It computes the delta to be back-propagated during *training* and, eventually, the updates to trainable weights
It usually receives as input only the global delta of the network, on which it performs a transformation, depending on the layer.

* **update** : this function is defined only for layers with trainable weights.

### Layers

Some text for introduction

* [Activation Layer](./NumPyNet/layers/activation_layer.md)
* [Avgpool Layer](./NumPyNet/layers/avgpool_layer.md)
* [BatchNorm Layer](./NumPyNet/layers/batchnorm_layer.md)
* [Connected Layer](./NumPyNet/layers/connected_layer.md)
* [Convolutional Layer](./NumPyNet/layers/convolutional_layer.md)
* [Cost Layer](./NumPyNet/layers/cost_layer.md)
* [DropOut Layer](./NumPyNet/layers/dropout_layer.md)
* [Input Layer](./NumPyNet/layers/input_layer.md)
* [L1norm Layer](./NumPyNet/layers/l1norm_layer.md)
* [L2norm Layer](./NumPyNet/layers/l2norm_layer.md)
* [Logistic Layer](./NumPyNet/layers/logistic_layer.md)
* [MaxPool Layer](./NumPyNet/layers/maxpool_layer.md)
* [Route Layer](./NumPyNet/layers/route_layer.md)
* [PixelShuffle Layer](./NumPyNet/layers/pixelshuffle_layer.md)
* [Shortcut Layer](./NumPyNet/layers/shortcut_layer.md)
* [UpSample Layer](./NumPyNet/layers/upsample-layer.md)
* [YOLO Layer](./NumPyNet/layers/yolo_layer.md)

### Installation

For a complete guide to the Python **installation** procedure see [here](./python_install.md).

### [Authors](./authors.md)

* **Nico Curti** [git](https://github.com/Nico-Curti), [unibo](https://www.unibo.it/sitoweb/nico.curti2)
* **Mattia Ceccarelli** [git](https://github.com/Mat092)

See also the list of [contributors](https://github.com/Nico-Curti/NumPyNet/contributors) [![GitHub contributors](https://img.shields.io/github/contributors/Nico-Curti/NumPyNet.svg?style=plastic)](https://github.com/Nico-Curti/NumPyNet/graphs/contributors/) who participated in this project.

### License

The `NumPyNet` package is licensed under the MIT "Expat" License. [![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/Nico-Curti/NumPyNet/blob/master/LICENSE.md)


#### Contributions

Any contribution is more than welcome. Just fill an issue or a pull request and I will check ASAP!

If you want update the list of layer objects please pay attention to the syntax of the layer class and to the names of member functions/variables used to prevent the compatibility with other layers and utility functions.


#### Acknowledgment

Thanks goes to all contributors of this project.

#### Citation

Please cite `NumPyNet` if you use it in your research.

```tex
@misc{NumPyNet,
  author = {Nico Curti and Mattia Ceccarelli},
  title = {NumPyNet - Neural Networks in Pure NumPy},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/Nico-Curti/NumPyNet}},
}
```
