# numeric_path is a base-three value 
#   with most-significant digit 
#   describing root and that ends in one
# base-three value
# 0: left child
# 1: current node
# 2: right child
# path_length describes number of edges involved in path
# note that path_length describes a certain amount of base three bits 
#   that does not include digit corresponding to trailing one; 
#   we will have to account for this trailing one manually
from ...Util import *
from Label import *
class PathLabel(Label):
  def __init__(self, numeric_path = None, path_length = None):
    value = (numeric_path, path_length)
    Label.__init__(self, value)
    self.numeric_path = numeric_path
    self.path_length = path_length
  def getValue(self):
    numeric_path = self.getNumericPath()
    path_length = self.getPathLength()
    value = (numeric_path, path_length)
    return value
  # takes O(1) time
  # ignore fact that we have O(log(n)) digits
  # note that we consider a numeric comparison as taking O(1) time
  def compare(self, x):
    curr_label_value = self.getValue()
    label_value = x.getValue()
    curr_numeric_path, curr_path_length = curr_label_value
    numeric_path, path_length = label_value
    # min_path_length = min(curr_path_length, path_length)
    # adding one is necessary to make sure a path length of zero does not mean we compare zeroes
    # min_path_length = min(curr_path_length, path_length) + 1
    min_path_length = min(curr_path_length, path_length)
    # curr_base_three_digits_without_leading_zeroes = PathLabel.toBaseThreeString(curr_numeric_path)
    # base_three_digits_without_leading_zeroes = PathLabel.toBaseThreeString(numeric_path)
    # know offset in terms of base-three digits based on path length
    # to truncate, we take difference between min. path length and path length for a particular numeric path
    # divide numeric paths by a power of three (i.e. path length minus min. path length)
    curr_truncated_numeric_path = PathLabel._toTruncatedBaseThreeValue(curr_numeric_path, min_path_length, curr_path_length)
    truncated_numeric_path = PathLabel._toTruncatedBaseThreeValue(numeric_path, min_path_length, path_length)
    """
    curr_num_base_three_digits_without_leading_zeroes = len(PathLabel.toBaseThreeString(curr_numeric_path))
    num_base_three_digits_without_leading_zeroes = len(PathLabel.toBaseThreeString(numeric_path))
    # print curr_num_base_three_digits_without_leading_zeroes
    # print num_base_three_digits_without_leading_zeroes
    curr_num_leading_zeroes = (curr_path_length + 1) - curr_num_base_three_digits_without_leading_zeroes
    num_leading_zeroes = (path_length + 1) - num_base_three_digits_without_leading_zeroes
    curr_leading_zero_str = "".join(["0"] * curr_num_leading_zeroes)
    leading_zero_str = "".join(["0"] * num_leading_zeroes)
    curr_full_numeric_path_str = curr_leading_zero_str + curr_base_three_digits_without_leading_zeroes
    full_numeric_path_str = leading_zero_str + base_three_digits_without_leading_zeroes
    # print curr_full_numeric_path_str, full_numeric_path_str
    curr_full_numeric_path_chars = list(curr_full_numeric_path_str)
    full_numeric_path_chars = list(full_numeric_path_str)
    curr_truncated_path_chars = curr_full_numeric_path_chars[0 : min_path_length]
    truncated_path_chars = full_numeric_path_chars[0 : min_path_length]
    curr_truncated_path_str = "".join(curr_truncated_path_chars)
    truncated_path_str = "".join(truncated_path_chars)
    curr_truncated_path = PathLabel.toBaseTenValue(curr_truncated_path_str)
    truncated_path = PathLabel.toBaseTenValue(truncated_path_str)
    # print PathLabel.toBaseThreeString(curr_truncated_path), PathLabel.toBaseThreeString(truncated_path)
    if curr_truncated_path == truncated_path:
      return 0
    elif curr_truncated_path < truncated_path:
      return -1
    elif curr_truncated_path > truncated_path:
      return 1
    """
    # print PathLabel.toBaseThreeString(curr_truncated_numeric_path), PathLabel.toBaseThreeString(truncated_numeric_path)
    if curr_truncated_numeric_path == truncated_numeric_path:
      return 0
    elif curr_truncated_numeric_path < truncated_numeric_path:
      return -1
    elif curr_truncated_numeric_path > truncated_numeric_path:
      return 1
  # takes O(1) time
  # ignore fact that we have O(log(n)) digits
  # note that we consider a numeric comparison as taking O(1) time
  @staticmethod
  def _toTruncatedBaseThreeValue(numeric_path, min_path_length, path_length):
    path_length_difference = path_length - min_path_length
    # print numeric_path, min_path_length, path_length
    # print path_length_difference
    power_of_three = 3 ** path_length_difference
    truncated_numeric_path = int(numeric_path / power_of_three)
    # print truncated_numeric_path
    return truncated_numeric_path
  # takes O(1) time
  # ignore fact that we have O(log(n)) digits
  # note that we consider a numeric comparison as taking O(1) time
  """
  def compare(self, x):
    curr_label_value = self.getValue()
    label_value = x.getValue()
    curr_numeric_path, curr_path_length = curr_label_value
    numeric_path, path_length = label_value
    # min_path_length = min(curr_path_length, path_length)
    # adding one is necessary to make sure a path length of zero does not mean we compare zeroes
    min_path_length = min(curr_path_length, path_length) + 1
    curr_base_three_digits_without_leading_zeroes = PathLabel.toBaseThreeString(curr_numeric_path)
    base_three_digits_without_leading_zeroes = PathLabel.toBaseThreeString(numeric_path)
    curr_num_base_three_digits_without_leading_zeroes = len(PathLabel.toBaseThreeString(curr_numeric_path))
    num_base_three_digits_without_leading_zeroes = len(PathLabel.toBaseThreeString(numeric_path))
    # print curr_num_base_three_digits_without_leading_zeroes
    # print num_base_three_digits_without_leading_zeroes
    curr_num_leading_zeroes = (curr_path_length + 1) - curr_num_base_three_digits_without_leading_zeroes
    num_leading_zeroes = (path_length + 1) - num_base_three_digits_without_leading_zeroes
    curr_leading_zero_str = "".join(["0"] * curr_num_leading_zeroes)
    leading_zero_str = "".join(["0"] * num_leading_zeroes)
    curr_full_numeric_path_str = curr_leading_zero_str + curr_base_three_digits_without_leading_zeroes
    full_numeric_path_str = leading_zero_str + base_three_digits_without_leading_zeroes
    # print curr_full_numeric_path_str, full_numeric_path_str
    curr_full_numeric_path_chars = list(curr_full_numeric_path_str)
    full_numeric_path_chars = list(full_numeric_path_str)
    curr_truncated_path_chars = curr_full_numeric_path_chars[0 : min_path_length]
    truncated_path_chars = full_numeric_path_chars[0 : min_path_length]
    curr_truncated_path_str = "".join(curr_truncated_path_chars)
    truncated_path_str = "".join(truncated_path_chars)
    curr_truncated_path = PathLabel.toBaseTenValue(curr_truncated_path_str)
    truncated_path = PathLabel.toBaseTenValue(truncated_path_str)
    # print PathLabel.toBaseThreeString(curr_truncated_path), PathLabel.toBaseThreeString(truncated_path)
    if curr_truncated_path == truncated_path:
      return 0
    elif curr_truncated_path < truncated_path:
      return -1
    elif curr_truncated_path > truncated_path:
      return 1
  """
  def setNumericPath(self, numeric_path):
    self.numeric_path = numeric_path
  def getNumericPath(self):
    return self.numeric_path
  def setPathLength(self, path_length):
    self.path_length = path_length
  def getPathLength(self):
    return self.path_length
  # assume that value is a non-negative integer
  # number has no leading zeroes
  @staticmethod
  def toBaseThreeString(value):
    return PathLabel._toBaseThreeStringHelper(value, "")
  @staticmethod
  def _toBaseThreeStringHelper(value, partial_str):
    if value == 0:
      return partial_str
    else:
      curr_digit = value % 3
      next_value = (value - value % 3) / 3
      next_partial_str = str(curr_digit) + partial_str
      return PathLabel._toBaseThreeStringHelper(next_value, next_partial_str)
  @staticmethod
  def toBaseTenValue(base_three_str):
    base_three_digit_char_list = list(base_three_str)
    # print base_three_digit_char_list
    value = PathLabel._toBaseTenValueHelper(base_three_digit_char_list, 0)
    return value
  @staticmethod
  def _toBaseTenValueHelper(partial_base_three_digit_char_list, curr_value):
    num_chars = len(partial_base_three_digit_char_list)
    if num_chars == 0:
      return curr_value
    else:
      curr_base_three_digit_char = partial_base_three_digit_char_list[0]
      # print curr_base_three_digit_char
      curr_base_three_digit = int(curr_base_three_digit_char)
      next_partial_base_three_digit_char_list = partial_base_three_digit_char_list[1 : ]
      return PathLabel._toBaseTenValueHelper(next_partial_base_three_digit_char_list, curr_value * 3 + curr_base_three_digit)
"""
print PathLabel.toBaseThreeString(1)
print PathLabel.toBaseThreeString(4)
print PathLabel.toBaseThreeString(16)
print PathLabel.toBaseThreeString(64)
print PathLabel.toBaseThreeString(256)
print PathLabel.toBaseThreeString(1024)
print PathLabel.toBaseThreeString(128)
"""
"""
print PathLabel.toBaseThreeString(1)
print PathLabel.toBaseThreeString(3)
print PathLabel.toBaseThreeString(243)
print PathLabel.toBaseTenValue("1")
print PathLabel.toBaseTenValue("10")
print PathLabel.toBaseTenValue("100000")
"""
# print PathLabel.toBaseThreeString(4097)
"""
label1 = PathLabel(PathLabel.toBaseTenValue("102011"), 8)
label2 = PathLabel(PathLabel.toBaseTenValue("102021"), 8)
print label1.compare(label2)
label1 = PathLabel(PathLabel.toBaseTenValue("102021"), 8)
label2 = PathLabel(PathLabel.toBaseTenValue("102021"), 8)
print label1.compare(label2)
label1 = PathLabel(PathLabel.toBaseTenValue("102021"), 8)
label2 = PathLabel(PathLabel.toBaseTenValue("102011"), 8)
print label1.compare(label2)
label1 = PathLabel(PathLabel.toBaseTenValue("001011"), 6)
label2 = PathLabel(PathLabel.toBaseTenValue("0010111"), 7)
print label1.compare(label2)
label1 = PathLabel(PathLabel.toBaseTenValue("0001011"), 7)
label2 = PathLabel(PathLabel.toBaseTenValue("0010111"), 7)
print label1.compare(label2)
"""
"""
import time
import random
time1 = time.clock()
for i in range(140000):
  curr_x = random.randint(0, 3 ** 8 - 1)
  x = random.randint(0, 3 ** 8 - 1)
  # curr_label = PathLabel(PathLabel.toBaseTenValue(PathLabel.toBaseThreeString(curr_x)), 8)
  # label = PathLabel(PathLabel.toBaseTenValue(PathLabel.toBaseThreeString(x)), 8)
  curr_label = PathLabel(curr_x, 8)
  label = PathLabel(x, 8)
  compare = curr_label.compare(label)
time2 = time.clock()
diff_time = time2 - time1
print diff_time
# let n be 30000
# compare against having an empty method body
# exponentiation-based method takes around twice as long
# string-based method takes ~10 times as long
# result is that we have a ~5 times speed-up
# in particular, results are 4.57 seconds vs. 0.702 seconds
"""
"""
# let n be 420000
# exponentiation-based method takes around 9.98 seconds
"""
"""
# let n be 140000
# exponentiation-based method takes around 3.28 seconds
"""
"""
# ('20021', 4), ('200221', 5), ('2002221', 6)
label1 = PathLabel(PathLabel.toBaseTenValue("20021"), 4)
label2 = PathLabel(PathLabel.toBaseTenValue("200221"), 5)
label3 = PathLabel(PathLabel.toBaseTenValue("2002221"), 6)
print label1.compare(label2)
print label2.compare(label3)
print label1.compare(label3)
print label2.compare(label1)
print label3.compare(label2)
print label3.compare(label2)
"""
