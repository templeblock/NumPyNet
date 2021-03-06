#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import timeit
import struct

__author__ = ['Nico Curti']
__email__ = ['nico.curti2@unibo.it']
__package__ = 'fast_math'


def pow2 (x):
  offset = 1     if x < 0.    else 0
  clipp  = -126. if x < -126. else x
  z      = clipp - int(clipp) + offset

  packed_x = struct.pack('i', int((1 << 23) * (clipp + 121.2740575 + 27.7280233 / (4.84252568 - z) - 1.49012907 * z)))
  return struct.unpack('f', packed_x)[0]

def exp (x):
  return pow2(1.442695040 * x)

def log2 (x):
  packed_x = struct.pack('f', x)
  i = struct.unpack('i', packed_x)[0]
  mx = (i & 0x007FFFFF) | 0x3f000000
  packed_x = struct.pack('i', mx)

  f = struct.unpack('f', packed_x)[0]
  i *= 1.1920928955078125e-7
  return i - 124.22551499 - 1.498030302 * f - 1.72587999 / (0.3520887068 + f);

def log (x):
  packed_x = struct.pack('f', x)
  i  = struct.unpack('i', packed_x)[0]
  y  = (i - 1064992212.25472) / (1092616192. - 1064992212.25472)
  ey = exp(y)
  y -= (ey - x) / ey
  ey = exp(y)
  y -= (ey - x) / ey
  ey = exp(y)
  y -= (ey - x) / ey
  ey = exp(y)
  y -= (ey - x) / ey
  return y

def pow (a, b):
  return pow2(b * log2(a))

def log10 (x):
  packed_x = struct.pack('f', x)
  i   = struct.unpack('i', packed_x)[0]
  y   = (i - 1064992212.25472) / (1092616192. - 1064992212.25472)
  y10 = pow(10, y)
  y -= (y10 - x) / (2.302585092994046 * y10)
  y10 = pow(10, y)
  y -= (y10 - x) / (2.302585092994046 * y10)
  return y

def atanh (x): # consequentially wrong
  return .5 * log((1. + x) / (1. - x))

def tanh (x):
  e = exp(-2 * x)
  return (1. - e) / (1. + e)

def hardtanh (x):

  if   x >= -1 and x <= 1.: return x
  elif x <  -1            : return -1.
  else                    : return 1.

def sqrt (x):

  xhalf = .5 * x

  packed_x = struct.pack('f', x)
  i = struct.unpack('i', packed_x)[0]  # treat float's bytes as int
  i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
  packed_i = struct.pack('i', i)
  y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float

  y = y * (1.5 - (xhalf * y * y))  # Newton's method
  y = y * (1.5 - (xhalf * y * y))  # Newton's method
  return x * y

def rsqrt (x):

  xhalf = .5 * x

  packed_x = struct.pack('f', x)
  i = struct.unpack('i', packed_x)[0]  # treat float's bytes as int
  i = 0x5f3759df - (i >> 1)            # arithmetic with magic number
  packed_i = struct.pack('i', i)
  y = struct.unpack('f', packed_i)[0]  # treat int's bytes as float

  y = y * (1.5 - (xhalf * y * y))  # Newton's method
  y = y * (1.5 - (xhalf * y * y))  # Newton's method
  return y


def _timing_np (func, args=None):
  SETUP_CODE = '''
import numpy as np

def np_pow2 (x):
  return 2 ** x

def np_rsqrt (x):
  return 1. / np.sqrt(x)

func = eval('{func}')
arr  = range(0, 10000)
'''.format(**{'func' : func})

  if args is not None:
    TEST_CODE = '''
y = map(lambda x : func(x, {args}), arr)
'''.format(**{'args' : args})
  else:
    TEST_CODE = '''
y = map(func, arr)
'''

  return timeit.repeat(setup=SETUP_CODE,
                       stmt=TEST_CODE,
                       repeat=100,
                       number=1000)

def _timing_fmath (func, args=None):
  SETUP_CODE = '''
from __main__ import {func}

arr = range(0, 10000)
'''.format(**{'func' : func})

  if args is not None:
    TEST_CODE = '''
y = map(lambda x : {func}(x, {args}), arr)
'''.format(**{'func' : func, 'args' : args})
  else:
    TEST_CODE = '''
y = map({func}, arr)
'''.format(**{'func' : func})

  return timeit.repeat(setup=SETUP_CODE,
                       stmt=TEST_CODE,
                       repeat=100,
                       number=1000)


if __name__ == '__main__':

  import numpy as np

  x = np.pi
  c = 1e-2

  assert np.isclose(2**x,               pow2(x),    atol=1e-3)
  assert np.isclose(np.exp(x),          exp(x),     atol=1e-5)
  assert np.isclose(x**.2,              pow(x, .2), atol=1e-4)
  assert np.isclose(np.log2(x),         log2(x),    atol=1e-4)
  assert np.isclose(np.log10(x),        log10(x),   atol=1e-3)
  assert np.isclose(np.log(x),          log(x),     atol=1e-4)
  assert np.isclose(np.arctanh(x*c),    atanh(x*c), atol=1e-4)
  assert np.isclose(np.tanh(x),         tanh(x),    atol=1e-5)
  assert np.isclose(np.sqrt(x),         sqrt(x),    atol=1e-5)
  assert np.isclose(1. / np.sqrt(x),    rsqrt(x),   atol=1e-5)


  np_pow2     = min(_timing_np(    'np_pow2'   ))
  fmath_pow2  = min(_timing_fmath( 'pow2'      ))
  np_exp      = min(_timing_np(    'np.exp'    ))
  fmath_exp   = min(_timing_fmath( 'exp'       ))
  np_pow      = min(_timing_np(    'np.power', .2))
  fmath_pow   = min(_timing_fmath( 'pow'     , .2))
  np_log2     = min(_timing_np(    'np.log2'   ))
  fmath_log2  = min(_timing_fmath( 'log2'      ))
  np_log10    = min(_timing_np(    'np.log10'  ))
  fmath_log10 = min(_timing_fmath( 'log10'     ))
  np_log      = min(_timing_np(    'np.log'    ))
  fmath_log   = min(_timing_fmath( 'log'       ))
  np_atanh    = min(_timing_np(    'np.arctanh'))
  fmath_atanh = min(_timing_fmath( 'atanh'     ))
  np_tanh     = min(_timing_np(    'np.tanh'   ))
  fmath_tanh  = min(_timing_fmath( 'tanh'      ))
  np_sqrt     = min(_timing_np(    'np.sqrt'   ))
  fmath_sqrt  = min(_timing_fmath( 'sqrt'      ))
  np_rsqrt    = min(_timing_np(    'np_rsqrt'  ))
  fmath_rsqrt = min(_timing_fmath( 'rsqrt'     ))

  print('                   CMath     FMath')
  print('pow2  function : {:.9f}     {:.9f}'.format(np_pow2, fmath_pow2))
  print('exp   function : {:.9f}     {:.9f}'.format(np_exp, fmath_exp))
  print('pow   function : {:.9f}     {:.9f}'.format(np_pow, fmath_pow))
  print('log2  function : {:.9f}     {:.9f}'.format(np_log2, fmath_log2))
  print('log10 function : {:.9f}     {:.9f}'.format(np_log10, fmath_log10))
  print('log   function : {:.9f}     {:.9f}'.format(np_log, fmath_log))
  print('atanh function : {:.9f}     {:.9f}'.format(np_atanh, fmath_atanh))
  print('tanh  function : {:.9f}     {:.9f}'.format(np_tanh, fmath_tanh))
  print('sqrt  function : {:.9f}     {:.9f}'.format(np_sqrt, fmath_sqrt))
  print('rsqrt function : {:.9f}     {:.9f}'.format(np_rsqrt, fmath_rsqrt))

  #                    CMath           FMath
  # pow2  function : 0.000387600     0.000341400
  # exp   function : 0.000342000     0.000346200
  # pow   function : 0.000583300     0.000539600
  # log2  function : 0.000380200     0.000382200
  # log10 function : 0.000384900     0.000341400
  # log   function : 0.000380500     0.000342200
  # atanh function : 0.000427400     0.000377600
  # tanh  function : 0.000372500     0.000375100
  # sqrt  function : 0.000372100     0.000341400
  # rsqrt function : 0.000376100     0.000341800
