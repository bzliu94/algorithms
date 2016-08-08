import math
import decimal
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
# truncates the value x to have n digits after the decimal point
def truncate(x, n):
  d = decimal.Decimal(str(x))
  result = d.quantize(decimal.Decimal(str(pow(10, -1 * n))), rounding = decimal.ROUND_DOWN)
  value = float(result)
  return value
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
