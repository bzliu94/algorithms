from core.Util import *

class Label:

  def __init__(self, value):

    self.value = value

  def setValue(self, value):

    self.value = value

  def getValue(self):

    return self.value

  # compare current label to provided label

  # output: -1, 0, or 1

  # -1: current label is less than provided label

  # 0: current label matches provided label

  # 1: current label is greater than provided label

  def compare(self, x):

    curr_value = self.getValue()

    value = x.getValue()

    return comp(curr_value, value)

  def toString(self):

    return self.getValue()

