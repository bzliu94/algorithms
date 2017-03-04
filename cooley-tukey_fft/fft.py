# inspired by jeremy kun

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


