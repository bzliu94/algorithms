import math
def comp(a, b):
  if a < b:
    return -1
  elif a == b:
    return 0
  elif a > b:
    return 1
def getDistance(loc1, loc2):
  x1, y1 = loc1
  x2, y2 = loc2
  delta_x = x2 - x1
  delta_y = y2 - y1
  distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
  return distance
import decimal
# round a value x to haven digits after decimal point
# round away from zero except if last significant digit is >= 5, otherwise round towards zero
# can be useful when dealing with multiple dimensions
def round_with_precision(x, n):
  """
  d = decimal.Decimal(str(x))
  result = d.quantize(decimal.Decimal(str(pow(10, -1 * n))), rounding = decimal.ROUND_HALF_DOWN)
  value = float(result)
  return value
  """
  # actually uses banker's rounding
  return round(x, n)
"""
# truncate a value x to have n digits after the decimal point
# note: paradoxically, ROUND_DOWN rounds toward zero
def truncate(x, n):
  # print x, n
  # value = float(math.trunc(x * pow(10, n))) / pow(10, n)
  # return value
  d = decimal.Decimal(str(x))
  result = d.quantize(decimal.Decimal(str(pow(10, -1 * n))), rounding = decimal.ROUND_DOWN)
  value = float(result)
  return value
"""
"""
print truncate(1, 2)
print truncate(1.001, 2)
print truncate(1.001, 3)
print truncate(1.001, 4)
print truncate(100.001, 2)
print truncate(100.001, 3)
print truncate(100.001, 4)
print truncate(-100.001, 1)
print truncate(-100.001, 2)
print truncate(-100.001, 3)
print truncate(-100.001, 4)
print truncate(10500, 0)
print truncate(10500, 1)
print truncate(10500, 2)
print truncate(10500.000009, 3)
print truncate(10500.000009, 4)
print truncate(10500.000009, 5)
print truncate(10500.000009, 6)
print truncate(10500.000009, 7)
"""
