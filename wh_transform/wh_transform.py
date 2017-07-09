# 2017-07-07

# fast walsh-hadamard transform and hard-coded inverse transform

# signal = [1, 0, 1, 0, 0, 1, 1, 0]

# 11_2 = 3

# signal1 = [1, 1, 0, 0, 0, 0, 0, 0]

signal1 = [0, 1, 0, 0, 1, 0, 0, 0]

# 10100_2 = 20

signal2 = [1, 0, 0, 0, 0, 0, 0, 0]

# signal = [0, 0, 1, 1, 0, 0, 1, 20]

# product is 3 * 20 = 60 = 111100_2 = 4 + 8 + 16 + 32 = 12 + 48 = 60

def getNextLayer(signal):

  num_elements = len(signal)

  next_layer = []

  for i in xrange(num_elements):
    curr_element = signal[i]
    next_element = None
    if i <= num_elements / 2 - 1:
      next_element = signal[i] + signal[i + num_elements / 2]
    else:
      next_element = signal[i - num_elements / 2] - signal[i]
    next_layer.append(next_element)

  return next_layer

# print getNextLayer([1, 1, 2, 0])

# print getNextLayer([3, 1])

import math

# we are assuming signal has size exactly equal to a power of two

def getLayers(signal, num_bump_levels = 0):
  num_elements = len(signal)
  num_layers = int(math.log(num_elements, 2))
  curr_signal = signal[ : ]
  layers = []
  layers.append(curr_signal)
  for i in xrange(num_bump_levels, num_layers):
    num_pieces = 2 ** i
    # print "num. pieces:", num_pieces
    pieces = []
    piece_size = num_elements / num_pieces
    for j in xrange(num_pieces):
      curr_piece = curr_signal[j * piece_size : (j + 1) * piece_size]
      next_piece = getNextLayer(curr_piece)
      pieces.append(next_piece)
    curr_layer = reduce(lambda x, y: x + y, pieces)
    layers.append(curr_layer)
    curr_signal = curr_layer
  return layers

layers1 = getLayers(signal1)

layers2 = getLayers(signal2)

print "layers #1:", layers1

print "layers #2:", layers2

# natural or hadamard ordering

W8 = [[1, 1, 1, 1, 1, 1, 1, 1], [1, -1, 1, -1, 1, -1, 1, -1], [1, 1, -1, -1, 1, 1, -1, -1], [1, -1, -1, 1, 1, -1, -1, 1], [1, 1, 1, 1, -1, -1, -1, -1], [1, -1, 1, -1, -1, 1, -1, 1], [1, 1, -1, -1, -1, -1, 1, 1], [1, -1, -1, 1, -1, 1, 1, -1]]

print "inverse hadamard matrix:", W8

coefficient = 1 / (1.0 * 2 ** (1.0 * 3))

print "inverse hadamard matrix coefficient:", coefficient

def dotProduct(a, b):
  a_list = list(a)
  b_list = list(b)
  num_terms = len(a_list)
  result = sum([a_list[i] * b_list[i] for i in xrange(num_terms)])
  return result

def scaleVector(v, k):
  v_list = list(v)
  next_v_list = [x * k for x in v_list]
  next_v = tuple(next_v_list)
  return next_v

def doComponentWiseMultiplication(a, b):
  a_list = list(a)
  b_list = list(b)
  num_terms = len(a_list)
  result = [a_list[i] * b_list[i] for i in xrange(num_terms)]
  next_result = tuple(result)
  return next_result

print "walsh signal #1:", layers1[3]

print "walsh signal #2:", layers2[3]

convolved_fd_signal = list(doComponentWiseMultiplication(layers1[3], layers2[3]))

print "convolved f.d. signal:", convolved_fd_signal

# print coefficient * dotProduct(layers[3], W8[0])

next_signal = []

def doInverseTransform(walsh_signal, inverse_hadamard_matrix_rows):
  next_signal = []
  num_elements = len(walsh_signal)
  for i in xrange(num_elements):
    walsh_function_vector = inverse_hadamard_matrix_rows[i]
    value = coefficient * dotProduct(walsh_signal, walsh_function_vector)
    next_value = int(value)
    next_signal.append(next_value)
  return next_signal

reconstructed_signal1 = doInverseTransform(layers1[3], W8)

reconstructed_signal2 = doInverseTransform(layers2[3], W8)

reconstructed_signal_result = doInverseTransform(convolved_fd_signal, W8)

print "reconstructed time-domain signal #1:", reconstructed_signal1

print "reconstructed time-domain signal #2:", reconstructed_signal2

print "reconstructed time-domain signal result:", reconstructed_signal_result

# signal = [1, 1, 2, 0, 1, -1, 0, 0]

signal = [1, 1, 0, 0, -1, 1, 0, 0]

layers = getLayers(signal, 1)

print "walsh signal:", layers

reconstructed_signal = doInverseTransform(layers[2], W8)

print "reconstructed signal:", reconstructed_signal

def fromBinaryToBaseTen(bits):
  num_bits = len(bits)
  value = 0
  for i in xrange(num_bits):
    curr_value = 2 ** i * bits[i]
    value += curr_value
  return value

# 1 + 4 + 32 + 64 = 5 + 96 = 101

value = fromBinaryToBaseTen(reconstructed_signal)

print "numerical value:", value


