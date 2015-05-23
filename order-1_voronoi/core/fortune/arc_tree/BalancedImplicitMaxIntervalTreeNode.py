# from ...tree.Node import *

from BalancedIntervalTreeNode import *

from ImplicitMaxIntervalRightEndpoint import *

class BalancedImplicitMaxIntervalTreeNode(BalancedIntervalTreeNode):

  def __init__(self, element, parent, left_child, right_child):

    BalancedIntervalTreeNode.__init__(self, element, parent, left_child, right_child)

  # an overridden method

  def createMaxRightEndpoint(self, max_value = None):

    # ignore max value

    max_right_endpoint = ImplicitMaxIntervalRightEndpoint()

    return max_right_endpoint

  # set a max value

  def setMaxValue(self, responsible_interval):

    max_right_endpoint = self.getMaxRightEndpoint()

    max_right_endpoint.setValue(max_value)

  # get a max value

  def getMaxValue(self):

    max_right_endpoint = self.getMaxRightEndpoint()

    max_value = max_right_endpoint.getValue()

    # print "max value:", max_value

    return max_value


