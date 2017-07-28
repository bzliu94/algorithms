# 2017-07-27

# added turning of frequency domain dot product to time domain dot product

# use parseval's theorem

# had a bug in complex dot product - were retrieving conjugates and then threw them away

# 2017-03-04

# inspired by jeremy kun

import math

import cmath
 
def omega(p, q):
  return cmath.exp((2.0 * cmath.pi * 1j * q) / p)

def fft(signal):
  n = len(signal)
  if n == 1:
    return signal
  else:
    F_even = fft([signal[i] for i in xrange(0, n, 2)])
    F_odd = fft([signal[i] for i in xrange(1, n, 2)])
    combined = [0] * n
    for m in xrange(n / 2):
      combined[m] = F_even[m] + omega(n, -m) * F_odd[m]
      combined[m + n / 2] = F_even[m] - omega(n, -m) * F_odd[m]
    return combined

def ifft(signal):
  timeSignal = fft([x.conjugate() for x in signal])
  return [x.conjugate() / len(signal) for x in timeSignal]

def dotProduct(a, b):
  a_list = list(a)
  b_list = list(b)
  num_terms = len(a_list)
  result = sum([a_list[i] * b_list[i] for i in xrange(num_terms)])
  return result

def doComplexDotProduct(a, b):
  b_list = list(b)
  next_b_list = [x.conjugate() for x in b]
  next_b = tuple(next_b_list)
  result = dotProduct(a, next_b)
  return result

def scaleVector(v, k):
  v_list = list(v)
  next_v_list = [x * k for x in v_list]
  next_v = tuple(next_v_list)
  return next_v

signal1 = [1, 1, 0, 0, 1, 1, 1, 0]

signal2 = [1, 1, 0, 0, 0, 1, 1, 1]

# note that scipy's fft algorithm gives same frequency domain dot product

print "signal #1:", signal1

print "signal #2:", signal2

value1 = dotProduct(signal1, signal2)

print "dot product in time domain:", value1

fd_signal1 = fft(signal1)

fd_signal2 = fft(signal2)

print "f.d. signal #1:", fd_signal1

print "f.d. signal #2:", fd_signal2

n = len(signal1)

print "dot product in frequency domain:", doComplexDotProduct(fd_signal1, fd_signal2).real / (1.0 * n)

"""

print fft([1, 0, 0, 0])

print fft([1, 0, 0, 0, 0, 0, 0, 0])

print fft([0, 1, 0, 0])

print fft([0, 1, 0, 0, 0, 0, 0, 0])

w = cmath.exp(2 * cmath.pi * 1j / 8)

print w

d = 4

print fft([w ** (k * d) for k in range(8)])

frequency_signal = fft([1, 0, 0, 0, 0, 0, 0, 0])

time_signal = ifft(frequency_signal)

print time_signal

real_time_signal = [x.real for x in time_signal]

print [int(round(x)) for x in real_time_signal]

"""


