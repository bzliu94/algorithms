# 2018-01-12

# modified example code

# we note that due to bertrand postulate, close prime is guaranteed to exist 
# and, as a result, we have good time overall for ntt

# 2017-11-28

# converted fft from cooley-tukey (via jeremy kun) to ntt

# inspired by pedro alves, project nayuki, yung-luen lan

# approach is recursive

# generator and modulus are reusable with signals that have lengths repeatedly halved; 
# chosen modulus that is larger than it needs to be w.r.t. current signal's length 
# is acceptable; also, given that the same modulus is used, we know that the generator 
# (which is still valid w.r.t. given prime modulus) from before can be used again

import math

# y is integer, q is prime; result is z = invMod(y, q) s.t. z * y == 1 (mod q)

def invMod(y, q):
  result = pow(int(y), q - 2, q)
  return result

def omega(g, mod, n):
  return pow(g, ((mod - 1) / n), mod)

# this is for ntt

def fft(signal, g, mod, for_ifft = False):
  n = len(signal)
  if n <= 1:
    return signal
  else:
    even = [signal[i] for i in xrange(0, n, 2)]
    odd = [signal[i] for i in xrange(1, n, 2)]
    F_even = fft(even, g, mod, for_ifft)
    F_odd = fft(odd, g, mod, for_ifft)
    combined = [0] * n
    for m in xrange(n / 2):
      curr_omega = omega(g, mod, n)
      if for_ifft == True:
        curr_omega = invMod(curr_omega, mod)
      omega_m = pow(curr_omega, m, mod)
      omega_m_odd_m = (omega_m * F_odd[m]) % mod
      combined[m] = (F_even[m] + omega_m_odd_m) % mod
      combined[m + n / 2] = (F_even[m] - omega_m_odd_m) % mod
    return combined

# this is for ntt

def ifft(signal, g, mod):
  scaler = invMod(len(signal), mod)
  next_signal = fft(signal, g, mod, True)
  result = [(x * scaler) % mod for x in next_signal]
  return result

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

def fromBinaryToBaseTen(bits):
  num_bits = len(bits)
  value = 0
  for i in xrange(num_bits):
    curr_value = 2 ** i * bits[i]
    value += curr_value
  return value

"""

signal1 = [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

signal2 = [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

print "signal #1:", signal1

print "signal #2:", signal2

# MOD here is N from nayuki
MOD = 673
# G here is g from nayuki
G = 5
# n here is size of signal
n = 16

fd_signal1 = fft(signal1, G, MOD)

fd_signal2 = fft(signal2, G, MOD)

print "f.d. signal #1:", fd_signal1

print "f.d. signal #2:", fd_signal2

n = len(signal1)

fd_signal3 = doComponentWiseMultiplication(fd_signal1, fd_signal2)

fd_signal3 = [x % MOD for x in fd_signal3]

print "f.d. signal #3:", fd_signal3

signal3 = ifft(fd_signal3, G, MOD)

print "t.d. signal #3:", signal3

value1 = fromBinaryToBaseTen(signal1)

value2 = fromBinaryToBaseTen(signal2)

value3 = fromBinaryToBaseTen(signal3)

print value1, value2, value3

print value1 * value2

"""

# returns smallest modulus N s.t. N = k * n + 1 and n is length of vector 
# for integer k >= 1, N > n, and N is prime; 
# though we have no good running time bound, dirichlet's theorem 
# guarantees that such a prime number must exist

def findModulus(veclen, minimum):
  start = (minimum - 1 + veclen - 1) // veclen
  i = max(start, 1)
  while True:
    n = i * veclen + 1
    if isPrime(n):
      return n
    i += 1

# returns arbitrary generator of multiplicative group of integers modulo N; 
# totient must be Euler's totient value of N; if N is prime, some generator must exist

def findGenerator(totient, mod):
  for i in range(1, mod):
    if isGenerator(i, totient, mod):
      return i

# determines whether value val is a generator for multiplicative group of integers modulo N; 
# given that totient is Euler's totient value of N and that mod is N, 
# check that the provided candidate val is a generator; 
# it raised to power of totient mod N ought to be one and 
# all prime factors p are s.t. val ^ (totient / p) != 1 mod N; 
# we note that totient for modulus N that is prime is N - 1

def isGenerator(val, totient, mod):
  pf = getUniquePrimeFactors(totient)
  return pow(val, totient, mod) == 1 and all((pow(val, totient // p, mod) != 1) for p in pf)

# returns list of distinct prime factors of provided integer in ascending order; 
# e.g., getUniquePrimeFactors(140) == [2, 5, 7]

def getUniquePrimeFactors(n):
  result = []
  i = 2
  end = int(math.sqrt(n))
  while i <= end:
    if n % i == 0:
      n //= i
      result.append(i)
      while n % i == 0:
        n //= i
      end = int(math.sqrt(n))
    i += 1
  if n > 1:
    result.append(n)
  return result

# determines whether given integer n >= 2 is prime

def isPrime(n):
  return all((n % i != 0) for i in range(2, int(math.sqrt(n)) + 1))

"""

signal1 = [4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

signal2 = [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# signal1 = [4, 1, 4, 2, 1, 3, 5, 6]

# signal2 = [6, 1, 8, 0, 3, 3, 9, 8]

# signal1 = [9, 9, 9, 9, 9, 9, 9, 9]

# signal2 = [9, 9, 9, 9, 9, 9, 9, 9]

print "t.d. signal #1:", signal1

print "t.d. signal #2:", signal2

min_mod = 10 ** 2 * 32 + 1

# min_mod = 9 ** 2 * 8 + 1

MOD = findModulus(len(signal1), min_mod)

G = findGenerator(MOD - 1, MOD)

# M = m ^ 2 * n + 1 OR M = m ^ 2 * n' + 1, where n' = 2 * n

print MOD, G

fd_signal1 = fft(signal1, G, MOD)

print "f.d. signal #1:", fd_signal1

fd_signal2 = fft(signal2, G, MOD)

print "f.d. signal #2:", fd_signal2

fd_signal3 = doComponentWiseMultiplication(fd_signal1, fd_signal2)

fd_signal3 = [x % MOD for x in fd_signal3]

print "f.d. signal #3:", fd_signal3

signal3 = ifft(fd_signal3, G, MOD)

print "t.d. signal #3:", signal3

value1 = fromBinaryToBaseTen(signal1)

value2 = fromBinaryToBaseTen(signal2)

value3 = fromBinaryToBaseTen(signal3)

print value1, value2, value3

print value1 * value2

"""


