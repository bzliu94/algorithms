# from ...tree.Node import *

from ...tree.OrderedBinarySearchTreeNode import *

from MaxIntervalRightEndpoint import *

from BalancedIntervalTreeNode import *

class BalancedIntervalTreeNode(OrderedBinarySearchTreeNode):

  """

  @staticmethod

  def construct(element, parent, left_child, right_child, max_value = None):

    max_right_endpoint = BalancedIntervalTreeNode.createMaxRightEndpoint(max_value)

    node = BalancedIntervalTreeNode(element, parent, left_child, right_child, max_right_endpoint)

    return node

  """

  def createMaxRightEndpoint(self, max_value = None):

    max_right_endpoint = MaxIntervalRightEndpoint(max_value)

    return max_right_endpoint

  def __init__(self, element, parent, left_child, right_child, max_value = None):

    OrderedBinarySearchTreeNode.__init__(self, element, parent, left_child, right_child)

    self.max_right_endpoint = self.createMaxRightEndpoint(max_value)

  def getMaxRightEndpoint(self):

    return self.max_right_endpoint

  def setMaxRightEndpoint(self, max_right_endpoint):

    self.max_right_endpoint = max_right_endpoint

  """

  # set a max value

  def setMaxValue(self, max_value):

    max_right_endpoint = self._getMaxRightEndpoint()

    max_right_endpoint.setValue(max_value)

  # get a max value

  def getMaxValue(self):

    max_right_endpoint = self._getMaxRightEndpoint()

    max_value = max_right_endpoint.getValue()

    return max_value

  """


